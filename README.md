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
The MSRJD note is reproducibly derived from the curated LaTeX source before the
site build:

```bash
python3 scripts/convert_msr_tex.py
uv run --with-requirements requirements-blog.txt python scripts/build_blog.py
```
