#!/usr/bin/env python3
"""Convert the curated MSRJD LaTeX note into the site's Markdown dialect."""

from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "content/martin-siggia-rose-formalism.tex"
OUTPUT = ROOT / "content/martin-siggia-rose-formalism.md"

SECTION_PATTERN = re.compile(r"^\\section\{(.+)\}$")
SUBSECTION_PATTERN = re.compile(r"^\\subsection\{(.+)\}$")
BEGIN_MATH_PATTERN = re.compile(r"^\\begin\{(equation\*?|align\*?)\}$")
END_MATH_PATTERN = re.compile(r"^\\end\{(equation\*?|align\*?)\}$")
LABEL_PATTERN = re.compile(r"\\label\{([^}]+)\}")
EQREF_PATTERN = re.compile(r"式(?:~|\s)*\\eqref\{([^}]+)\}")
BARE_EQREF_PATTERN = re.compile(r"\\eqref\{([^}]+)\}")


def clean_heading(text: str) -> str:
    match = re.fullmatch(r"\\texorpdfstring\{(.+)\}\{.+\}", text)
    if match:
        text = match.group(1)
    return clean_prose(text).replace("$", "") if text.count("$") == 2 else clean_prose(text)


def clean_prose(text: str) -> str:
    text = text.replace(r"It\^o", "Itô")
    text = text.replace(r"f\"ur", "für")
    text = text.replace(r"th\'eorie", "théorie")
    text = text.replace(r"ph\'enom\`enes", "phénomènes")
    text = re.sub(r"\\textbf\{([^{}]+)\}", r"**\1**", text)
    text = re.sub(r"\\emph\{([^{}]+)\}", r"*\1*", text)
    text = re.sub(r"\\href\{([^{}]+)\}\{([^{}]+)\}", r"[\2](\1)", text)
    text = text.replace("``", "“").replace("''", "”")
    text = text.replace("---", "—").replace("--", "–")
    text = text.replace("~", " ")
    return text


def collect_equation_numbers(lines: list[str]) -> dict[str, int]:
    labels: dict[str, int] = {}
    number = 0
    in_math = False
    numbered = False
    for raw in lines:
        line = raw.strip()
        begin = BEGIN_MATH_PATTERN.match(line)
        if begin:
            in_math = True
            numbered = not begin.group(1).endswith("*")
            if numbered:
                number += 1
            continue
        if in_math:
            label = LABEL_PATTERN.search(line)
            if label and numbered:
                labels[label.group(1)] = number
            if END_MATH_PATTERN.match(line):
                in_math = False
    return labels


def replace_references(text: str, labels: dict[str, int]) -> str:
    def replace(match: re.Match[str]) -> str:
        label = match.group(1)
        return f"式 [({labels[label]})](#equation-{label})"

    text = EQREF_PATTERN.sub(replace, text)

    def replace_bare(match: re.Match[str]) -> str:
        label = match.group(1)
        return f"[({labels[label]})](#equation-{label})"

    return BARE_EQREF_PATTERN.sub(replace_bare, text)


def render_math_block(
    environment: str,
    body: list[str],
    number: int | None,
) -> list[str]:
    label: str | None = None
    cleaned: list[str] = []
    for raw in body:
        match = LABEL_PATTERN.search(raw)
        if match:
            label = match.group(1)
            raw = LABEL_PATTERN.sub("", raw)
        raw = raw.replace(r"\nonumber", "")
        # Correct the one transcription typo without changing the mathematics.
        raw = raw.replace(r"\Jdet[x],\mathcal O[x]", r"\Jdet[x]\,\mathcal O[x]")
        if raw.strip():
            cleaned.append(raw.rstrip())

    if environment.startswith("align"):
        cleaned = [r"\begin{aligned}", *cleaned, r"\end{aligned}"]

    rendered: list[str] = ["$$", *cleaned, "$$"]
    if number is not None:
        anchor = f' id="equation-{label}"' if label else ""
        rendered.append(f'<p class="equation-number"{anchor}>({number})</p>')
    return rendered


def convert() -> str:
    source_lines = SOURCE.read_text(encoding="utf-8").splitlines()
    labels = collect_equation_numbers(source_lines)
    body_start = source_lines.index(r"\begin{document}") + 1
    lines = source_lines[body_start:]

    output = [
        "# Martin–Siggia–Rose formalism",
        "",
    ]
    equation_number = 0
    paragraph: list[str] = []
    in_abstract = False
    in_keybox = False
    in_bibliography = False
    math_environment: str | None = None
    math_body: list[str] = []

    def flush_paragraph() -> None:
        if not paragraph:
            return
        if in_keybox:
            joined = "> " + " ".join(part.removeprefix("> ").strip() for part in paragraph)
        else:
            joined = " ".join(part.strip() for part in paragraph)
        joined = replace_references(clean_prose(joined), labels)
        output.extend([joined, ""])
        paragraph.clear()

    for raw in lines:
        line = raw.strip()

        if math_environment is not None:
            if END_MATH_PATTERN.match(line):
                if not math_environment.endswith("*"):
                    equation_number += 1
                    current_number: int | None = equation_number
                else:
                    current_number = None
                output.extend(render_math_block(math_environment, math_body, current_number))
                output.append("")
                math_environment = None
                math_body = []
            else:
                math_body.append(raw)
            continue

        begin_math = BEGIN_MATH_PATTERN.match(line)
        if begin_math:
            flush_paragraph()
            math_environment = begin_math.group(1)
            continue

        if line in {r"\maketitle", r"\tableofcontents", r"\newpage", r"\end{document}"}:
            flush_paragraph()
            continue
        if line == r"\begin{abstract}":
            flush_paragraph()
            in_abstract = True
            continue
        if line == r"\end{abstract}":
            flush_paragraph()
            in_abstract = False
            continue
        if line == r"\begin{keybox}":
            flush_paragraph()
            in_keybox = True
            continue
        if line == r"\end{keybox}":
            flush_paragraph()
            in_keybox = False
            continue
        if line == r"\begin{thebibliography}{9}":
            flush_paragraph()
            in_bibliography = True
            output.extend(["## 参考文献", ""])
            continue
        if line == r"\end{thebibliography}":
            flush_paragraph()
            in_bibliography = False
            continue

        section = SECTION_PATTERN.match(line)
        subsection = SUBSECTION_PATTERN.match(line)
        if section or subsection:
            flush_paragraph()
            level = "##" if section else "###"
            title = (section or subsection).group(1)
            output.extend([f"{level} {clean_heading(title)}", ""])
            continue

        if in_bibliography and line.startswith(r"\bibitem"):
            flush_paragraph()
            output.append(f"{len([x for x in output if x.startswith('- ')]) + 1}. ")
            continue

        if not line:
            flush_paragraph()
            continue

        if in_keybox:
            paragraph.append("> " + line)
        elif in_bibliography:
            if output and re.fullmatch(r"\d+\. ", output[-1]):
                output[-1] += clean_prose(line)
            else:
                paragraph.append(line)
        else:
            paragraph.append(line)

    flush_paragraph()
    result = "\n".join(output).strip() + "\n"
    result = result.replace(">  **", "> **")
    return result


def main() -> None:
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(convert(), encoding="utf-8")


if __name__ == "__main__":
    main()
