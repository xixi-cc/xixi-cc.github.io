# Xixi Research Atlas

Personal academic homepage for Xixi Cao, published at <https://xixi-cc.github.io/>.

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
The MSRJD note is reproducibly derived from the curated LaTeX source before the
site build:

```bash
python3 scripts/convert_msr_tex.py
uv run --with-requirements requirements-blog.txt python scripts/build_blog.py
```
