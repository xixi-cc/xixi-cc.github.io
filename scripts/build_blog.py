#!/usr/bin/env python3
"""Render checked-in Markdown notes as static GitHub Pages articles."""

from __future__ import annotations

import html
import re
from dataclasses import dataclass
from pathlib import Path

import markdown
from latex2mathml.converter import convert as latex_to_mathml
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
    published_zh: str
    category: str
    social_description: str | None = None
    image: str | None = None


ARTICLES = (
    Article(
        slug="martin-siggia-rose-formalism",
        source="martin-siggia-rose-formalism.md",
        description="从 Langevin 方程出发，经泛函数 Delta 约束、响应场和高斯噪声积分，推导 MSRJD 动作量，并以 OU 过程检验相关与响应。",
        published="2026-08-28",
        published_zh="2026 年 8 月 28 日",
        category="统计场论",
    ),
    Article(
        slug="langevin-fokker-planck",
        source="langevin-fokker-planck.md",
        description="从 Itô 随机微分方程出发，用生成元与短时传播核两条路线推导 Fokker–Planck 方程，并讨论 Stratonovich 约定。",
        published="2026-08-28",
        published_zh="2026 年 8 月 28 日",
        category="随机过程",
    ),
    Article(
        slug="numerical-simulation-notes",
        source="numerical-simulation-notes.md",
        description="面向 C/C++ 科学计算的简明检查表：内存布局、并行、随机数、浮点精度、I/O 与可复现性。",
        published="2026-08-28",
        published_zh="2026 年 8 月 28 日",
        category="数值方法",
    ),
    Article(
        slug="structure-factor",
        source="structure-factor.md",
        description="从 Fourier 定义、实空间关联和超均匀性，到周期粒子模拟、壳平均与 Type-1 NUFFT 的结构因子笔记。",
        social_description="结构因子的定义、物理意义、有限尺寸效应与高精度数值计算。",
        published="2026-08-26",
        published_zh="2026 年 8 月 26 日",
        category="理论与数值方法",
        image="assets/blog/structure-factor-runtime.png",
    ),
)


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
    for old, new in replacements.items():
        source = source.replace(old, new)
    return source


def render_mathml(fragment: str) -> str:
    """Replace Arithmatex wrappers with static MathML for offline reading."""

    def replace(match: re.Match[str]) -> str:
        source = html.unescape(match.group("latex").strip())
        if source.startswith(r"\(") and source.endswith(r"\)"):
            return latex_to_mathml(normalize_latex(source[2:-2]), display="inline")
        if source.startswith(r"\[") and source.endswith(r"\]"):
            return latex_to_mathml(normalize_latex(source[2:-2]), display="block")
        raise ValueError(f"Unknown math delimiter: {source[:20]!r}")

    return ARITHMATEX_PATTERN.sub(replace, fragment)


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
    body = render_mathml(renderer.convert(body_source))
    for index, latex in enumerate(display_blocks):
        placeholder = f'<div data-math-block="{index}"></div>'
        body = body.replace(
            placeholder,
            latex_to_mathml(normalize_latex(latex), display="block"),
        )
    toc = renderer.toc

    title_html = markdown_renderer().convert(title_source)
    title_html = title_html.removeprefix("<p>").removesuffix("</p>")
    title_html = render_mathml(title_html)
    plain_title = html.unescape(re.sub(r"<[^>]+>", "", title_html))

    if article.slug == "structure-factor":
        replacements = {
            'src="assets/sk-runtime-scaling.png"': 'src="../../assets/blog/structure-factor-runtime.png"',
            'src="assets/sk-accuracy-scaling.png"': 'src="../../assets/blog/structure-factor-accuracy.png"',
        }
        for old, new in replacements.items():
            body = body.replace(old, new)
    body = body.replace("<img ", '<img loading="lazy" decoding="async" ')

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
    <link rel="icon" href="../../assets/favicon.svg" type="image/svg+xml">
    <link rel="stylesheet" href="../../styles.css">
    <link rel="stylesheet" href="../../blog.css">
    <script>
        window.MathJax = {{
            chtml: {{fontURL: '../../assets/mathjax/output/chtml/fonts/woff-v2'}},
            options: {{enableMenu: false}}
        }};
    </script>
    <script defer src="../../assets/mathjax/tex-mml-chtml.js"></script>
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
</body>
</html>
"""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(document, encoding="utf-8")


def main() -> None:
    for article in ARTICLES:
        render_article(article)


if __name__ == "__main__":
    main()
