#!/usr/bin/env python3
"""Render checked-in Markdown notes as static GitHub Pages articles."""

from __future__ import annotations

import html
import json
import re
from dataclasses import dataclass
from pathlib import Path

import markdown
from PIL import Image
from markdown.extensions.toc import slugify_unicode


ROOT = Path(__file__).resolve().parent.parent
ARITHMATEX_PATTERN = re.compile(
    r'<(?P<tag>span|div) class="arithmatex">(?P<latex>.*?)</(?P=tag)>',
    re.DOTALL,
)


@dataclass(frozen=True)
class Article:
    slug: str
    source: str
    description: str
    published: str
    category: str
    social_description: str | None = None
    image: str | None = None

    @property
    def published_zh(self) -> str:
        year, month, day = map(int, self.published.split("-"))
        return f"{year} 年 {month} 月 {day} 日"


def load_articles() -> tuple[Article, ...]:
    from datetime import date
    records = json.loads((ROOT / "content/articles.json").read_text(encoding="utf-8"))
    articles = tuple(Article(**record) for record in records)
    if len({a.slug for a in articles}) != len(articles):
        raise ValueError("Duplicate article slug")
    for article in articles:
        date.fromisoformat(article.published)
        if not re.fullmatch(r"[a-z0-9-]+", article.slug):
            raise ValueError(f"Invalid slug: {article.slug}")
        source = (ROOT / "content" / article.source).resolve()
        if not source.is_relative_to(ROOT / "content") or not source.is_file():
            raise ValueError(f"Invalid article source: {article.source}")
    return articles


ARTICLES = load_articles()


def markdown_renderer() -> markdown.Markdown:
    return markdown.Markdown(
        extensions=["extra", "sane_lists", "toc", "pymdownx.arithmatex"],
        extension_configs={
            "toc": {"slugify": slugify_unicode, "toc_depth": "2-3"},
            "pymdownx.arithmatex": {"generic": True},
        },
        output_format="html5",
    )


def normalize_markdown_math_blocks(source: str) -> str:
    """Remove incidental list indentation from display-math blocks."""
    result: list[str] = []
    in_display = False
    for raw in source.splitlines():
        if raw.strip() == "$$":
            in_display = not in_display
            result.append("$$")
        elif in_display:
            result.append(raw.lstrip())
        else:
            result.append(raw)
    if in_display:
        raise ValueError("Unclosed display-math block")
    return "\n".join(result)


def extract_display_math(source: str) -> tuple[str, list[str]]:
    """Protect display equations from Markdown's list and raw-HTML parsing."""
    blocks: list[str] = []
    output: list[str] = []
    current: list[str] = []
    in_display = False
    for raw in source.splitlines():
        if raw == "$$":
            if in_display:
                index = len(blocks)
                blocks.append("\n".join(current))
                output.append(f'<div data-math-block="{index}"></div>')
                current = []
            in_display = not in_display
        elif in_display:
            current.append(raw)
        else:
            output.append(raw)
    if in_display:
        raise ValueError("Unclosed display-math block")
    return "\n".join(output), blocks


def expand_balanced_macro(source: str, macro: str, left: str, right: str) -> str:
    """Expand a one-argument macro while respecting nested braces."""
    marker = f"\\{macro}{{"
    while marker in source:
        start = source.index(marker)
        cursor = start + len(marker)
        depth = 1
        while cursor < len(source) and depth:
            if source[cursor] == "{":
                depth += 1
            elif source[cursor] == "}":
                depth -= 1
            cursor += 1
        if depth:
            raise ValueError(f"Unclosed \\{macro} macro")
        argument = source[start + len(marker) : cursor - 1]
        source = source[:start] + left + argument + right + source[cursor:]
    return source


def normalize_latex(source: str) -> str:
    """Expand the small macro set used by the MSRJD source."""
    source = expand_balanced_macro(source, "avg", r"\left\langle ", r"\right\rangle")
    replacements = {
        r"\dd": r"\mathop{}\!\mathrm{d}",
        r"\ii": r"\mathrm{i}",
        r"\ee": r"\mathrm{e}",
        r"\D": r"\mathcal{D}",
        r"\E": r"\mathcal{E}",
        r"\Jdet": r"\mathcal{J}",
        r"\bm": r"\boldsymbol",
    }
    # Match complete TeX control words: \D must never consume \Delta.
    return re.sub(r"\\[A-Za-z]+", lambda m: replacements.get(m.group(0), m.group(0)), source)


def math_markup(source: str, display: str) -> str:
    """Preserve TeX for the bundled MathJax parser, including AMS alignment."""
    tag, left, right = ("div", r"\[", r"\]") if display == "block" else ("span", r"\(", r"\)")
    return f'<{tag} class="arithmatex">{left}{html.escape(normalize_latex(source))}{right}</{tag}>'


def render_math(fragment: str) -> str:
    """Normalize only protected math, then let MathJax parse the original TeX."""

    def replace(match: re.Match[str]) -> str:
        source = html.unescape(match.group("latex").strip())
        if source.startswith(r"\(") and source.endswith(r"\)"):
            return math_markup(source[2:-2], display="inline")
        if source.startswith(r"\[") and source.endswith(r"\]"):
            return math_markup(source[2:-2], display="block")
        raise ValueError(f"Unknown math delimiter: {source[:20]!r}")

    return ARITHMATEX_PATTERN.sub(replace, fragment)


def optimize_images(body: str, output_path: Path) -> str:
    """Build responsive WebP derivatives; retain original scientific figures."""
    def replace(match: re.Match[str]) -> str:
        tag = match.group(0)
        src_match = re.search(r'src="([^"]+)"', tag)
        if not src_match:
            return tag
        src = src_match.group(1)
        if src.startswith(("http:", "https:", "data:")):
            return tag
        path = (output_path.parent / src).resolve()
        if not path.is_relative_to(ROOT / "assets"):
            return tag
        with Image.open(path) as original:
            width, height = original.size
            variants = []
            for size in sorted({min(width, n) for n in (640, 1280, 2080, width)}):
                target = path.with_name(f"{path.stem}-{size}.webp")
                if not target.exists() or target.stat().st_mtime < path.stat().st_mtime:
                    resized = original.copy()
                    if size < width:
                        resized = original.resize((size, round(height * size / width)), Image.Resampling.LANCZOS)
                    resized.save(target, "WEBP", lossless=True, method=6)
                variants.append(f"{src.rsplit('/', 1)[0]}/{target.name} {size}w")
        tag = tag.replace("<img ", f'<img loading="lazy" decoding="async" width="{width}" height="{height}" ')
        sources = html.escape(", ".join(variants), quote=True)
        return f'<picture><source type="image/webp" srcset="{sources}" sizes="(max-width: 620px) calc(100vw - 28px), (max-width: 914px) calc(100vw - 64px), 850px">{tag}</picture>'
    return re.sub(r"<img\b[^>]*>", replace, body)


def render_article(article: Article) -> None:
    source_path = ROOT / "content" / article.source
    output_path = ROOT / "blog" / article.slug / "index.html"
    source = source_path.read_text(encoding="utf-8")
    lines = source.splitlines()
    if not lines or not lines[0].startswith("# "):
        raise ValueError(f"{source_path}: note must begin with a level-one title")

    title_source = lines[0][2:].strip()
    body_source = normalize_markdown_math_blocks("\n".join(lines[1:]).strip())
    body_source, display_blocks = extract_display_math(body_source)
    renderer = markdown_renderer()
    body = render_math(renderer.convert(body_source))
    for index, latex in enumerate(display_blocks):
        placeholder = f'<div data-math-block="{index}"></div>'
        body = body.replace(
            placeholder,
            math_markup(latex, display="block"),
        )
    toc = renderer.toc

    title_html = markdown_renderer().convert(title_source)
    title_html = title_html.removeprefix("<p>").removesuffix("</p>")
    title_html = render_math(title_html)
    plain_title = html.unescape(re.sub(r"<[^>]+>", "", title_html))

    if article.slug == "structure-factor":
        replacements = {
            'src="assets/sk-runtime-scaling.png"': 'src="../../assets/blog/structure-factor-runtime.png"',
            'src="assets/sk-accuracy-scaling.png"': 'src="../../assets/blog/structure-factor-accuracy.png"',
        }
        for old, new in replacements.items():
            body = body.replace(old, new)
    if article.slug == "harnessvla-to-zetta":
        body = body.replace(
            'src="assets/',
            'src="../../assets/blog/harnessvla-to-zetta/',
        )
    body = optimize_images(body, output_path)

    canonical = f"https://xixi-cc.github.io/blog/{article.slug}/"
    social_description = article.social_description or article.description
    image_meta = ""
    twitter_card = "summary"
    if article.image:
        image_url = f"https://xixi-cc.github.io/{article.image}"
        image_meta = (
            f'\n    <meta property="og:image" content="{image_url}">'
            f'\n    <meta name="twitter:image" content="{image_url}">'
        )
        twitter_card = "summary_large_image"

    structured_data = json.dumps(
        {
            "@context": "https://schema.org",
            "@type": "Article",
            "headline": plain_title,
            "description": article.description,
            "datePublished": article.published,
            "dateModified": article.published,
            "inLanguage": "zh-CN",
            "url": canonical,
            "mainEntityOfPage": canonical,
            "author": {
                "@type": "Person",
                "name": "Xineng Cao",
                "alternateName": ["Xixi Cao", "曹溪能"],
                "url": "https://xixi-cc.github.io/",
            },
        },
        ensure_ascii=False,
    )

    math_scripts = ""
    if 'class="arithmatex"' in body or 'class="arithmatex"' in title_html:
        math_scripts = """    <script>
        window.MathJax = {
            chtml: {fontURL: '../../assets/mathjax/output/chtml/fonts/woff-v2'},
            options: {enableMenu: false}
        };
    </script>
    <script defer src="../../assets/mathjax/tex-mml-chtml.js"></script>
"""

    document = f"""<!doctype html>
<html lang="zh-CN">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{html.escape(plain_title)} · 曹溪能</title>
    <meta name="description" content="{html.escape(article.description)}">
    <meta property="og:type" content="article">
    <meta property="og:url" content="{canonical}">
    <meta property="og:title" content="{html.escape(plain_title)}">
    <meta property="og:description" content="{html.escape(social_description)}">{image_meta}
    <meta property="article:published_time" content="{article.published}">
    <meta name="twitter:card" content="{twitter_card}">
    <meta name="twitter:title" content="{html.escape(plain_title)}">
    <meta name="twitter:description" content="{html.escape(social_description)}">
    <link rel="canonical" href="{canonical}">
    <script type="application/ld+json">{structured_data}</script>
    <link rel="icon" href="../../assets/favicon.svg" type="image/svg+xml">
    <link rel="stylesheet" href="../../styles.css">
    <link rel="stylesheet" href="../../blog.css">
{math_scripts}
</head>
<body class="article-page">
    <header class="topbar">
        <nav aria-label="主导航">
            <a href="../../">主页</a>
            <a href="../../#reading">论文追踪</a>
            <a href="../../#blog" aria-current="page">博客</a>
        </nav>
    </header>

    <main class="article-shell">
        <article class="blog-article">
            <header class="article-header">
                <p class="article-kicker"><a href="../../#blog">研究笔记</a></p>
                <h1>{title_html}</h1>
                <p class="article-meta"><time datetime="{article.published}">{article.published_zh}</time> · {article.category}</p>
            </header>

            <details class="article-outline">
                <summary>文章目录</summary>
                {toc}
            </details>

            <div class="article-layout">
                <div class="article-content">
                    {body}
                </div>
            </div>

            <footer class="article-footer">
                <a href="../../#blog">← 返回博客</a>
                <a href="../../rights.html">版权与引用</a>
                <a href="https://github.com/xixi-cc/xixi-cc.github.io">查看主页源码</a>
            </footer>
        </article>
    </main>
    <!-- Cloudflare Web Analytics -->
    <script type="module" src="https://static.cloudflareinsights.com/beacon.min.js" data-cf-beacon='{{"token":"73522e5dee9b42b0be84b4847e4dd502"}}'></script>
    <!-- End Cloudflare Web Analytics -->
</body>
</html>
"""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(document, encoding="utf-8")


def render_homepage() -> None:
    rows = []
    for article in ARTICLES:
        # The Markdown H1 is the only title source, including inline mathematics.
        title = (ROOT / "content" / article.source).read_text(encoding="utf-8").splitlines()[0][2:].strip()
        title = html.escape(title.replace("$", ""))
        rows.append(f'''                <article>
                    <time datetime="{article.published}">{article.published.replace("-", ".")}</time>
                    <div>
                        <h3><a href="blog/{article.slug}/">{title}</a></h3>
                        <p>{html.escape(article.description)}</p>
                    </div>
                </article>''')
    path = ROOT / "index.html"
    source = path.read_text(encoding="utf-8")
    start, end = "<!-- BEGIN GENERATED BLOG -->", "<!-- END GENERATED BLOG -->"
    if source.count(start) != 1 or source.count(end) != 1:
        raise ValueError("Homepage must contain one generated blog region")
    before, rest = source.split(start)
    _, after = rest.split(end)
    path.write_text(before + start + "\n" + "\n".join(rows) + "\n            " + end + after, encoding="utf-8")


def main() -> None:
    for article in ARTICLES:
        render_article(article)
    render_homepage()
    sitemap_entries = [
        ("https://xixi-cc.github.io/", "2026-08-29"),
        ("https://xixi-cc.github.io/rights.html", "2026-08-29"),
        *[(f"https://xixi-cc.github.io/blog/{article.slug}/", article.published) for article in ARTICLES],
    ]
    sitemap = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]
    for url, last_modified in sitemap_entries:
        sitemap.extend(
            [
                "  <url>",
                f"    <loc>{html.escape(url)}</loc>",
                f"    <lastmod>{last_modified}</lastmod>",
                "  </url>",
            ]
        )
    sitemap.append("</urlset>")
    (ROOT / "sitemap.xml").write_text("\n".join(sitemap) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
