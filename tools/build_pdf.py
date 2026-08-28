#!/usr/bin/env python3
"""Convertit les Markdown des labos en PDF.

Chaîne : Markdown -> HTML (python-markdown) -> PDF (google-chrome --headless).

Arborescence attendue : labs/<labo>/<fr|nl|en>/0X-*.md  (+ labs/<labo>/files/)

Usage :
    python3 tools/build_pdf.py                       # tout le dossier labs/
    python3 tools/build_pdf.py labs/04-dockerfile     # un labo, les 3 langues
    python3 tools/build_pdf.py labs/04-dockerfile/nl  # un labo, une langue
    python3 tools/build_pdf.py labs/04-dockerfile/fr/01-theorie.md

Encadrés : une citation Markdown qui commence par une étiquette en gras
(`> **Linux** — …`) devient un encadré typé. Étiquettes reconnues :
  - note  : À retenir / Onthouden / Remember
  - warn  : Piège / Valkuil / Pitfall
  - podman: Podman
  - domain: n'importe quelle autre étiquette (Linux, Java, Réseau, Windows / WSL,
            Sécurité, Histoire, Spring Boot, Angular, HTTP…) — affichée comme
            un petit label de domaine au-dessus du texte.
"""

from __future__ import annotations

import html
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
LANGS = ("fr", "nl", "en")

CHROME_CANDIDATES = [
    "google-chrome",
    "google-chrome-stable",
    "chromium",
    "chromium-browser",
]

NOTE_LABELS = {"à retenir", "a retenir", "onthouden", "remember", "key point"}
WARN_LABELS = {"piège", "piege", "valkuil", "pitfall", "attention", "let op", "warning"}
PODMAN_LABELS = {"podman"}

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<title>{title}</title>
<style>
{css}
</style>
</head>
<body class="lang-{lang}">
{body}
</body>
</html>
"""

CALLOUT_RE = re.compile(
    r"<blockquote>\s*<p><strong>([^<]{1,40})</strong>\s*(?:&mdash;|—|–|-|:)\s*",
    re.IGNORECASE,
)


def classify(label: str) -> str:
    key = html.unescape(label).strip().lower()
    if key in NOTE_LABELS:
        return "note"
    if key in WARN_LABELS:
        return "warn"
    if key in PODMAN_LABELS:
        return "podman"
    return "domain"


SPLIT_RE = re.compile(
    r"</p>\s*<p><strong>([^<]{1,40})</strong>\s*(?:&mdash;|—|–)\s*"
)


def split_merged_callouts(body: str) -> str:
    """Deux citations consécutives séparées par une ligne vide sont fusionnées par
    python-markdown en un seul <blockquote>. On les re-sépare quand un paragraphe
    interne commence par une étiquette d'encadré."""

    def fix(m: re.Match) -> str:
        inner = m.group(1)
        inner = SPLIT_RE.sub(
            lambda k: f"</p>\n</blockquote>\n<blockquote>\n<p><strong>{k.group(1)}</strong> — ",
            inner,
        )
        return f"<blockquote>{inner}</blockquote>"

    return re.sub(r"<blockquote>(.*?)</blockquote>", fix, body, flags=re.DOTALL)


def apply_callouts(body: str) -> str:
    body = split_merged_callouts(body)

    def repl(m: re.Match) -> str:
        label = html.unescape(m.group(1)).strip()
        kind = classify(label)
        return (
            f'<blockquote class="callout callout-{kind}" '
            f'data-label="{html.escape(label, quote=True)}">\n<p>'
        )

    return CALLOUT_RE.sub(repl, body)


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


def lang_of(md_file: Path) -> str:
    parent = md_file.parent.name
    return parent if parent in LANGS else "fr"


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
    body = apply_callouts(md.convert(text))

    first_line = text.lstrip().split("\n", 1)[0]
    title = first_line.lstrip("# ").strip() or md_file.stem

    html_doc = HTML_TEMPLATE.format(
        lang=lang_of(md_file), title=html.escape(title), css=css, body=body
    )
    pdf_file = md_file.with_suffix(".pdf")

    with tempfile.TemporaryDirectory() as tmp:
        tmp_html = Path(tmp) / "page.html"
        tmp_html.write_text(html_doc, encoding="utf-8")
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
    if md_file.name.startswith("01-") and pages > 5:
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
    # Seuls les Markdown places dans un dossier de langue sont des documents de labo.
    return [f for f in files if f.parent.name in LANGS and f.name[:2].isdigit()]


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
