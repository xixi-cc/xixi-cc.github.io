#!/usr/bin/env python3
"""Render the checked-in Markdown note as a static GitHub Pages article."""

from __future__ import annotations

from pathlib import Path

import markdown
from markdown.extensions.toc import slugify_unicode


ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "content/structure-factor.md"
OUTPUT = ROOT / "blog/structure-factor/index.html"


def markdown_renderer() -> markdown.Markdown:
    return markdown.Markdown(
        extensions=["extra", "sane_lists", "toc", "pymdownx.arithmatex"],
        extension_configs={
            "toc": {"slugify": slugify_unicode, "toc_depth": "2-3"},
            "pymdownx.arithmatex": {"generic": True},
        },
        output_format="html5",
    )


def main() -> None:
    source = SOURCE.read_text(encoding="utf-8")
    lines = source.splitlines()
    if not lines or not lines[0].startswith("# "):
        raise ValueError("The note must begin with a level-one title")

    title_source = lines[0][2:].strip()
    body_source = "\n".join(lines[1:]).strip()
    renderer = markdown_renderer()
    body = renderer.convert(body_source)
    toc = renderer.toc

    title_html = markdown_renderer().convert(title_source)
    title_html = title_html.removeprefix("<p>").removesuffix("</p>")

    replacements = {
        'src="assets/sk-runtime-scaling.png"': 'src="../../assets/blog/structure-factor-runtime.png"',
        'src="assets/sk-accuracy-scaling.png"': 'src="../../assets/blog/structure-factor-accuracy.png"',
    }
    for old, new in replacements.items():
        body = body.replace(old, new)
    body = body.replace("<img ", '<img loading="lazy" decoding="async" ')

    document = f"""<!doctype html>
<html lang="zh-CN">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>静态与动态结构因子 S(k) · 曹溪能</title>
    <meta name="description" content="从 Fourier 定义、实空间关联和超均匀性，到周期粒子模拟、壳平均与 Type-1 NUFFT 的结构因子笔记。">
    <meta property="og:type" content="article">
    <meta property="og:url" content="https://xixi-cc.github.io/blog/structure-factor/">
    <meta property="og:title" content="静态与动态结构因子 S(k)">
    <meta property="og:description" content="结构因子的定义、物理意义、有限尺寸效应与高精度数值计算。">
    <meta property="og:image" content="https://xixi-cc.github.io/assets/blog/structure-factor-runtime.png">
    <meta property="article:published_time" content="2026-08-26">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="静态与动态结构因子 S(k)">
    <meta name="twitter:description" content="结构因子的定义、物理意义、有限尺寸效应与高精度数值计算。">
    <meta name="twitter:image" content="https://xixi-cc.github.io/assets/blog/structure-factor-runtime.png">
    <link rel="canonical" href="https://xixi-cc.github.io/blog/structure-factor/">
    <link rel="icon" href="../../assets/favicon.svg" type="image/svg+xml">
    <link rel="stylesheet" href="../../styles.css">
    <link rel="stylesheet" href="../../blog.css">
    <script>
        window.MathJax = {{
            tex: {{
                inlineMath: [['\\\\(', '\\\\)']],
                displayMath: [['\\\\[', '\\\\]']]
            }},
            options: {{
                skipHtmlTags: ['script', 'noscript', 'style', 'textarea', 'pre', 'code']
            }}
        }};
    </script>
    <script defer src="https://cdn.jsdelivr.net/npm/mathjax@3.2.2/es5/tex-mml-chtml.js"></script>
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
                <p class="article-meta"><time datetime="2026-08-26">2026 年 8 月 26 日</time> · 理论与数值方法</p>
            </header>

            <details class="mobile-toc">
                <summary>文章目录</summary>
                {toc}
            </details>

            <div class="article-layout">
                <aside class="article-toc" aria-label="文章目录">
                    <strong>文章目录</strong>
                    {toc}
                </aside>
                <div class="article-content">
                    {body}
                </div>
            </div>

            <footer class="article-footer">
                <a href="../../#blog">← 返回博客</a>
                <a href="https://github.com/xixi-cc/xixi-cc.github.io">查看主页源码</a>
            </footer>
        </article>
    </main>
</body>
</html>
"""
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(document, encoding="utf-8")


if __name__ == "__main__":
    main()
