#!/usr/bin/env python3
"""Convertit les Markdown des labos en PDF.

Chaîne : Markdown -> HTML (python-markdown) -> PDF (google-chrome --headless).

Usage :
    python3 tools/build_pdf.py                 # tout le dossier labs/
    python3 tools/build_pdf.py labs/04-dockerfile
    python3 tools/build_pdf.py labs/04-dockerfile/01-theorie.md
"""

from __future__ import annotations

import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import markdown

ROOT = Path(__file__).resolve().parent.parent
CSS = ROOT / "assets" / "pdf.css"
LABS = ROOT / "labs"

CHROME_CANDIDATES = [
    "google-chrome",
    "google-chrome-stable",
    "chromium",
    "chromium-browser",
]

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="utf-8">
<title>{title}</title>
<style>
{css}
</style>
</head>
<body>
{body}
</body>
</html>
"""


def find_chrome() -> str:
    for name in CHROME_CANDIDATES:
        path = shutil.which(name)
        if path:
            return path
    sys.exit("Erreur : aucun navigateur Chrome/Chromium trouve pour generer les PDF.")


def count_pages(pdf: Path) -> int:
    """Compte approximatif des pages d'un PDF non compresse en objets."""
    data = pdf.read_bytes()
    pages = len(re.findall(rb"/Type\s*/Page[^s]", data))
    return pages if pages else -1


def render(md_file: Path, chrome: str, css: str) -> None:
    text = md_file.read_text(encoding="utf-8")
    md = markdown.Markdown(
        extensions=[
            "fenced_code",
            "codehilite",
            "tables",
            "attr_list",
            "sane_lists",
            "md_in_html",
        ],
        extension_configs={"codehilite": {"guess_lang": False}},
    )
    body = md.convert(text)

    first_line = text.lstrip().split("\n", 1)[0]
    title = first_line.lstrip("# ").strip() or md_file.stem

    html = HTML_TEMPLATE.format(title=title, css=css, body=body)
    pdf_file = md_file.with_suffix(".pdf")

    with tempfile.TemporaryDirectory() as tmp:
        tmp_html = Path(tmp) / "page.html"
        tmp_html.write_text(html, encoding="utf-8")
        cmd = [
            chrome,
            "--headless",
            "--disable-gpu",
            "--no-sandbox",
            "--no-pdf-header-footer",
            f"--user-data-dir={tmp}/profile",
            f"--print-to-pdf={pdf_file}",
            tmp_html.as_uri(),
        ]
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
        if not pdf_file.exists():
            print(proc.stderr[-2000:], file=sys.stderr)
            sys.exit(f"Echec de generation pour {md_file}")

    pages = count_pages(pdf_file)
    flag = ""
    if md_file.name.startswith("01-theorie") and pages > 5:
        flag = "  <-- TROP LONG (max 5 pages)"
    rel = pdf_file.relative_to(ROOT)
    print(f"  {rel}  ({pages} p.){flag}")


def collect(args: list[str]) -> list[Path]:
    if not args:
        targets = [LABS]
    else:
        targets = [Path(a).resolve() for a in args]

    files: list[Path] = []
    for target in targets:
        if target.is_file() and target.suffix == ".md":
            files.append(target)
        elif target.is_dir():
            files.extend(sorted(target.rglob("*.md")))
        else:
            print(f"Ignore : {target}", file=sys.stderr)
    return [f for f in files if f.name != "README.md"]


def main() -> None:
    chrome = find_chrome()
    css = CSS.read_text(encoding="utf-8")
    files = collect(sys.argv[1:])
    if not files:
        sys.exit("Aucun fichier Markdown a convertir.")
    print(f"Generation de {len(files)} PDF...")
    current_dir = None
    for md_file in files:
        if md_file.parent != current_dir:
            current_dir = md_file.parent
            print(f"\n[{current_dir.relative_to(ROOT)}]")
        render(md_file, chrome, css)
    print("\nTermine.")


if __name__ == "__main__":
    main()
