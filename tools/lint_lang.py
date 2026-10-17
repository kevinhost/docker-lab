#!/usr/bin/env python3
"""Repère les calques et faux amis classiques dans les Markdown des labos.

Usage :
    python3 tools/lint_lang.py                # tout labs/
    python3 tools/lint_lang.py labs/04-*      # un labo (trois langues)
    python3 tools/lint_lang.py labs/04-*/nl   # une langue
    python3 tools/lint_lang.py --all …        # inclut les règles « ? » (à vérifier en contexte)

La langue est déduite du dossier parent (fr/, nl/, en/). Les blocs de code
(``` … ```), le code en ligne (`…`) et les lignes de sortie citées sont ignorés :
on ne lint que la prose. Chaque motif est accompagné de la tournure attendue.

Ce n'est PAS un correcteur : c'est un filet qui attrape les calques « connus ».
La relecture sans la version source à côté (CLAUDE.md, section 2) reste
obligatoire. Les listes s'allongent à chaque calque rencontré en relecture.
Deux niveaux : les règles sûres (un calque avéré, à corriger) et les règles
préfixées « ? » (mot correct dans un sens, calque dans l'autre : à relire en
contexte, affichées seulement avec --all). Code de sortie : 1 s'il y a au moins
un signalement sûr, 0 sinon.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LABS = ROOT / "labs"

# (regex insensible à la casse, remplacement attendu)
RULES: dict[str, list[tuple[str, str]]] = {
    # --- Français : calques de l'anglais (la doc source est en anglais) ---
    "fr": [
        (r"\bsupport(e|ent|é|ée|és|ées|er)\b(?! (pas|plus) )", "« prend en charge », « gère » (support = prendre en charge, pas supporter)"),
        (r"\bsupporté[es]?\b", "« pris en charge »"),
        (r"\blibrairies?\b", "« bibliothèque » (library)"),
        (r"\bdigital(e|es|aux)?\b", "« numérique »"),
        (r"\badress(e|er|ent|é|ée)\b (un|le|ce|les|des) (problème|besoin|cas|sujet)", "« traiter », « s'attaquer à » (to address)"),
        (r"\bfai(t|re|sant) (du|beaucoup de) sens\b", "« a du sens », « est logique » (makes sense)"),
        (r"\bdéfinitivement\b", "? définitivement = pour de bon (OK) ; pour *definitely* dire « sans aucun doute »"),
        (r"\bversatile[s]?\b", "« polyvalent » (versatile FR = changeant)"),
        (r"\bconfusant[es]?\b", "« déroutant », « source de confusion »"),
        (r"\bassum(e|ent|er|ez|ons) que\b", "« suppose que », « part du principe que » (to assume)"),
        (r"\bopportunité de\b", "« occasion de » (opportunity)"),
        (r"\bdélivr(e|er|ent|é|ée)\b (une|la|le|des|l')", "« livrer », « fournir » (deliver)"),
        (r"\biniti(e|er|ent|é|ée)\b (le|la|un|une|les)", "« lancer », « démarrer », « amorcer » (initiate)"),
        (r"\bcompléter\b (le|la|l'|un|une) (étape|labo|installation|déploiement|tâche)", "« terminer » (complete)"),
        (r"\bdramatique(ment)?\b", "« spectaculaire », « radicalement » (dramatic)"),
        (r"\bcustomis(e|er|ation|é|ée)\b", "« personnaliser »"),
        (r"\bmonitor(e|er|ing|é|ée)\b", "« surveiller », « supervision »"),
        (r"\bcheck(e|er|ez|é|ée)\b", "« vérifier »"),
        (r"\bforward(e|er|é|ée)\b", "« transférer », « rediriger »"),
        (r"\bupdat(e|er|é|ée)\b", "« mettre à jour »"),
        (r"\bsett(e|er|é|ée)\b (la|le|une|un)", "« définir », « positionner »"),
        (r"\bau final\b", "« finalement », « en fin de compte »"),
        (r"\ben charge de\b", "« chargé de », « responsable de »"),
        (r"\bbas(é|ée|és|ées) sur\b", "? « fondé sur », « construit à partir de » (acceptable, à limiter)"),
        (r"\bpas de (souci|problème) (à|pour)\b", "reformuler (no problem to…)"),
        (r"\bune fois que (le|la|les) .{0,40} (est|sont) (fait|faits|terminé|terminés|prêt|prêts)\b", "« une fois … terminé » sans « que » (once X is done)"),
        (r"\bréalis(e|er|ez|ent|é) que\b", "« se rendre compte que » (to realize)"),
        (r"\bactuellement\b", "? « actuellement » = maintenant ; pour *actually* dire « en fait »"),
        (r"\béventuellement\b", "? « éventuellement » = peut-être ; pour *eventually* dire « finalement »"),
        (r"\bglobalement\b", "? pour *globally* dire « au niveau global », « pour tout le système »"),
        (r"\btechnologie[s]? (de )?(conteneur|container)", "« les conteneurs » (container technology)"),
        (r"\bdans le (cas|but) d'", "« pour », « afin de » (lourd)"),
        (r"\bil est (possible|nécessaire) de\b", "reformuler à la voix active (« vous pouvez », « il faut »)"),
        (r"\brouler (un|le|des) conteneur", "« lancer », « faire tourner » (québécisme)"),
    ],
    # --- Néerlandais : calques de l'anglais et gallicismes ---
    "nl": [
        (r"\bsupporte?(ert|ren|erde|erd)\b", "« ondersteunt », « ondersteunen »"),
        (r"\b(maakt|maken|maakte) (geen |veel )?zin\b", "« is logisch », « slaat ergens op » (makes sense)"),
        (r"\badresse(ert|ren|erde|erd)\b", "« aanpakken », « behandelen » (to address)"),
        (r"\bactueel\b", "? « actueel » = d'actualité ; pour *actually* dire « eigenlijk »"),
        (r"\beventueel\b", "? « eventueel » = le cas échéant ; pour *eventually* dire « uiteindelijk »"),
        (r"\bdefinitief\b", "? definitief = pour de bon (OK) ; pour *definitely* dire « zeker », « absoluut »"),
        (r"\bpunctueel\b", "« waar nodig », « alleen wanneer het nodig is »"),
        (r"\bin functie van\b", "« afhankelijk van », « naargelang » (gallicisme)"),
        (r"\bop het niveau van\b", "« bij », « in », « wat … betreft » (gallicisme)"),
        (r"\bter hoogte van\b", "« bij », « in » (gallicisme, sauf sens spatial)"),
        (r"\bnoteer dat\b", "« merk op dat », « let op: » (notez que)"),
        (r"\bop het einde\b", "« aan het einde », « uiteindelijk » (flandricisme)"),
        (r"\bwerkpost\b", "« werkstation », « pc » (gallicisme poste de travail)"),
        (r"\bverwittig(t|en|d)\b", "« waarschuwt », « meldt » (flandricisme)"),
        (r"\bruntt?\b|\brunnen\b|\brunde\b", "« draait », « draaien », « uitvoeren » (hors commande `run`)"),
        (r"\bcheck(t|en|te)\b", "« controleer », « nagaan »"),
        (r"\bgedediceerd\b|\bdedicated\b", "« specifiek », « eigen », « toegewijd »"),
        (r"\bbest practices\b", "« goede gewoonten », ou garder en italique comme terme"),
        (r"\bin eerste instantie\b", "? acceptable ; vérifier que ce n'est pas « dans un premier temps » mécanique"),
        (r"\bhet is mogelijk om\b|\bhet is nodig om\b", "reformuler à l'actif (« je kunt », « je moet »)"),
        (r"\bik wil zeggen\b", "« ik bedoel » (je veux dire)"),
        (r"\bmen (kan|moet|ziet)\b", "« je kunt », « je moet », « je ziet » (on = je, pas men)"),
        (r"\bu\b|\buw\b", "tutoiement « je »/« jouw » dans toute la série"),
    ],
    # --- Anglais : calques du français ---
    "en": [
        (r"\bpermits? to\b|\ballows? to\b", "« lets you », « allows you to » (permet de)"),
        (r"\bin a first time\b|\bin a second time\b", "« first », « then » (dans un premier temps)"),
        (r"\bat the level of\b", "« in », « at », « for » (au niveau de)"),
        (r"\bprecise[sd]? (that|the|which|how)\b", "« specify », « state » (préciser)"),
        (r"\bconserves?\b", "« keep », « retain » (conserver)"),
        (r"\bpunctually\b", "« when needed », « case by case »"),
        (r"\bwithout appeal\b", "« final », « no reprieve »"),
        (r"\binterlocutor\b", "« no one to talk to », « counterpart »"),
        (r"\breading grid\b", "« mental model », « frame »"),
        (r"\bit is possible to\b|\bit is necessary to\b", "« you can », « you must » (il est possible de)"),
        (r"\bwe remark\b|\bremark that\b", "« note that » (remarquer)"),
        (r"\bthe (same|latter) one\b", "« the same », « the latter »"),
        (r"\bactually\b", "? « actually » = en fait, pas « actuellement » (currently)"),
        (r"\beventually\b", "? « eventually » = finalement, pas « éventuellement » (possibly)"),
        (r"\bdispose of\b", "« have », « has » (disposer de ≠ dispose of = jeter)"),
        (r"\brealise?s? an?\b", "« perform », « carry out » (réaliser)"),
        (r"\bnotion of\b", "? « concept of », « idea of » (notion de)"),
        (r"\bin the frame(work)? of\b", "« as part of », « within » (dans le cadre de)"),
        (r"\bmore and more\b", "« increasingly » (de plus en plus)"),
        (r"\bthanks to\b", "? « because of », « using » (grâce à, acceptable avec parcimonie)"),
        (r"\bthe fact that\b", "? reformuler (le fait que)"),
    ],
}

FENCE = re.compile(r"^\s*(```|~~~)")
INLINE_CODE = re.compile(r"`[^`]*`")
URL = re.compile(r"https?://\S+")


def lang_of(path: Path) -> str | None:
    for part in path.parts:
        if part in RULES:
            return part
    return None


def lint_file(path: Path, show_all: bool) -> int:
    lang = lang_of(path)
    if lang is None:
        return 0
    rules = [(re.compile(p, re.IGNORECASE), hint) for p, hint in RULES[lang]
             if show_all or not hint.startswith("?")]
    hits = 0
    in_code = False
    for n, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if FENCE.match(raw):
            in_code = not in_code
            continue
        if in_code:
            continue
        line = URL.sub("", INLINE_CODE.sub("", raw))
        for rx, hint in rules:
            for m in rx.finditer(line):
                print(f"{path.relative_to(ROOT)}:{n}: « {m.group(0)} » → {hint}")
                if not hint.startswith("?"):
                    hits += 1
    return hits


def main(argv: list[str]) -> int:
    show_all = "--all" in argv
    targets = [Path(a) for a in argv if a != "--all"] or [LABS]
    files: list[Path] = []
    for t in targets:
        t = t if t.is_absolute() else ROOT / t
        files += sorted(t.rglob("*.md")) if t.is_dir() else [t]
    total = sum(lint_file(f, show_all) for f in files if f.suffix == ".md")
    print(f"\n{total} calque(s) sûr(s) dans {len(files)} fichier(s)"
          + ("" if show_all else " (--all pour voir aussi les « ? »)") + ".")
    return 1 if total else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
