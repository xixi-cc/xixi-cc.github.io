# Xixi Research Atlas

Personal academic homepage for Xixi Cao, published at <https://xixi-cc.github.io/>.

## License and citation

Original editorial content is available under CC BY-NC 4.0, while original
site code is available under MIT. Third-party materials are excluded. See
[LICENSE.md](LICENSE.md) for scope and [CITATION.md](CITATION.md) or
[CITATION.cff](CITATION.cff) for the preferred attribution format.

## Local preview

```bash
python3 -m http.server 8000
```

Open <http://localhost:8000/>. Changes pushed to `main` are published by GitHub Pages.

## Rebuild the blog articles

```bash
uv run --with-requirements requirements-blog.txt python scripts/build_blog.py
```

Editable sources live under `content/`; generated pages live under `blog/<slug>/`.
`content/articles.json` is the single metadata source for order, slug, source,
description, publication date, category and optional social image/description.
The title comes only from the Markdown H1; display dates are derived from the ISO date.
The same build generates the marked homepage blog list and sitemap. Do not edit
that generated region or the article HTML by hand. Add a note by creating its
Markdown source and one metadata record, then run the build below.
The MSRJD note is reproducibly derived from the curated LaTeX source before the
site build:

```bash
python3 scripts/convert_msr_tex.py
uv run --with-requirements requirements-blog.txt python scripts/build_blog.py
```

The blog build also generates losslessly encoded WebP image variants beside the
original figures (640, 1280, 2080 pixels, and original width, deduplicated).
Generated HTML uses responsive sources, lazy decoding/loading, and intrinsic
image dimensions. Keep originals and generated variants together when releasing;
original PNGs remain the fallback. Existing variants are reused unless the source
image is newer. MathJax is included only in articles containing mathematics.

Homepage secondary text is black via a `.home-page` scoped variable; blog
font choices remain independent in `blog.css`. Blog prose uses the selected
book-style Georgia / Chinese serif stack at 18px with 1.9 line height (17px on
mobile), paired with the existing MathJax TeX formula fonts. All illustrations
and their original source files are retained.

Formula rendering retains escaped TeX in protected Arithmatex wrappers and feeds
it directly to the bundled MathJax 3.2.2 TeX input processor. Do not reintroduce
the lossy intermediate latex2mathml conversion: it lost `aligned` tables.
Custom macros must match entire control words (`\D` is distinct from `\Delta`).
The local `input/tex/extensions/boldsymbol.js` is the matching MathJax 3.2.2
extension, obtained from https://cdn.jsdelivr.net/npm/mathjax@3.2.2/es5/input/tex/extensions/boldsymbol.js
and covered by `assets/mathjax/LICENSE`.

After changing formula rendering, run the macro regressions and browser audit:

```bash
uv run --with-requirements requirements-blog.txt python scripts/test_blog_math.py
uv run --with playwright python scripts/check_blog_rendering.py
```

The browser audit serves the site temporarily on loopback, checks every article
at desktop/mobile widths, and fails on missing resources, formula errors,
unrendered expressions, broken Delta/aligned output, or page overflow.
