# Xixi Research Atlas

Personal academic homepage for Xixi Cao, published at <https://xixi-cc.github.io/>.

## Local preview

```bash
python3 -m http.server 8000
```

Open <http://localhost:8000/>. Changes pushed to `main` are published by GitHub Pages.

## Rebuild the blog article

```bash
uv run --with-requirements requirements-blog.txt python scripts/build_blog.py
```

The editable source is `content/structure-factor.md`; the generated page is
`blog/structure-factor/index.html`.
