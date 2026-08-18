# CLAUDE.md — Série de labos Docker (CLI)

Ce dépôt contient une série de labos d'auto-formation Docker, en français, orientés
**ligne de commande**. Objectif final : comprendre Docker tel qu'il est utilisé en
entreprise sur une stack **Spring Boot + Angular + PostgreSQL**, tout en gardant chaque
labo **simple et centré sur Docker** (jamais sur Java, ni sur TypeScript).

---

## 1. Public et objectif

- **Apprenant** : développeur qui connaît le terminal Linux, découvre Docker.
- **But** : maîtriser les concepts fondamentaux + le vocabulaire employé en entreprise.
- **Non-but** : apprendre Kubernetes, Swarm, Java ou Angular. On y fait référence, on ne
  les enseigne pas.

## 2. Format imposé (à respecter pour CHAQUE labo)

Chaque labo produit **4 PDF**, générés à partir de 4 fichiers Markdown :

| Fichier source        | PDF produit           | Rôle |
|-----------------------|-----------------------|------|
| `01-theorie.md`       | `01-theorie.pdf`      | Cours théorique à apprendre. **4 à 5 pages max.** Peut contenir des commandes en illustration, mais **pas d'exercice**. |
| `02-questions.md`     | `02-questions.pdf`    | Questions de contrôle sur la théorie. **Pas faciles** : elles doivent prouver la compréhension, pas la mémorisation. |
| `03-reponses.md`      | `03-reponses.pdf`     | Corrigé détaillé : réponse + explication + nuance + exemple concret pour chaque question. |
| `04-labo-pratique.md` | `04-labo-pratique.pdf`| Manipulation guidée au terminal, avec vérifications attendues. |

Plus, si nécessaire :

- `files/` : fichiers de base fournis pour le labo pratique (Dockerfile, compose,
  sources minimales…). Quand la création du fichier **est** l'exercice, le labo demande
  à l'apprenant de l'écrire ; sinon le fichier est fourni ici, prêt à l'emploi.

### Arborescence

```
docker-lab/
├── CLAUDE.md
├── README.md                  # sommaire + mode d'emploi
├── build.sh                   # génère tous les PDF
├── tools/build_pdf.py         # Markdown -> HTML -> PDF (Chrome headless)
├── assets/pdf.css             # mise en page des PDF
└── labs/
    ├── 01-conteneurs-et-architecture/
    │   ├── 01-theorie.md      (+ .pdf)
    │   ├── 02-questions.md    (+ .pdf)
    │   ├── 03-reponses.md     (+ .pdf)
    │   ├── 04-labo-pratique.md(+ .pdf)
    │   └── files/
    └── ...
```

## 3. Chaîne de génération des PDF

```bash
./build.sh              # tout reconstruire
./build.sh labs/03-*    # reconstruire un labo
```

- `build.sh` crée `.venv/` au besoin (`markdown`, `pygments`) puis lance
  `tools/build_pdf.py`.
- Conversion : Markdown → HTML (extensions `fenced_code`, `tables`, `attr_list`,
  `sane_lists`, `codehilite`) → PDF via `google-chrome --headless --print-to-pdf`.
- **Ne jamais éditer un `.pdf` à la main** : il est régénéré. La source de vérité est le
  `.md`.
- Après génération, **vérifier le nombre de pages** de `01-theorie.pdf` (le script
  l'affiche). S'il dépasse 5, raccourcir le Markdown — pas la CSS.

### Conventions Markdown utilisées par le gabarit

- `# Titre` : titre du document (une seule fois, en tête).
- `## Section` : commence **toujours** une nouvelle section ; pas de saut de page forcé
  sauf `<div class="page-break"></div>`.
- Blocs de code : toujours annotés (` ```bash `, ` ```dockerfile `, ` ```yaml `).
- Encadrés : `> **À retenir** — …` pour les points clés, `> **Piège** — …` pour les
  erreurs classiques. Le CSS les met en valeur.
- Tableaux : privilégiés pour les comparaisons (commande / effet / quand l'utiliser).

## 4. Règles de rédaction

**Théorie**
- Français clair, phrases courtes. Le jargon anglais reste en anglais (*image*, *layer*,
  *registry*, *bind mount*…) avec la traduction à la première occurrence.
- Chaque document commence par « Objectifs » (3-5 puces) et finit par « À retenir »
  (5-7 puces) + « Vocabulaire ».
- Toujours expliquer le **pourquoi**, pas seulement le comment.
- Un lien explicite avec l'entreprise dans une courte section « En entreprise » :
  comment ce concept se traduit sur une stack Spring Boot / Angular.
- 4-5 pages A4 = environ 1300-1700 mots + code.

**Questions**
- 10 à 14 questions, numérotées, difficulté croissante.
- Types imposés : questions de raisonnement (« que se passe-t-il si… »), de diagnostic
  (« voici une sortie de commande / un Dockerfile, qu'est-ce qui cloche ? »), de
  comparaison (« X vs Y, dans quel cas… »), et de prédiction de résultat.
- **Interdit** : questions dont la réponse est un mot recopié du cours, QCM triviaux.
- Indiquer entre crochets le niveau : `[Compréhension]`, `[Analyse]`, `[Diagnostic]`.

**Réponses**
- Pour chaque question : **Réponse** (courte et nette) → **Pourquoi** (le mécanisme) →
  **Nuance / piège** → **Exemple** (commande, sortie ou extrait de fichier).
- Ne jamais se contenter d'affirmer : montrer la commande qui prouve la réponse.

**Labo pratique**
- Étapes numérotées, chacune avec : la ou les commandes, ce qu'on doit observer, et une
  phrase d'explication.
- Toujours terminer par une section « Nettoyage » (`docker rm`, `docker rmi`,
  `docker system prune`) pour ne pas laisser la machine encombrée.
- Tout doit tourner sur **une seule machine Linux avec Docker Engine**, sans compte
  payant, sans cloud, avec des images publiques légères (`alpine`, `nginx:alpine`,
  `postgres:16-alpine`, `eclipse-temurin`, `node:22-alpine`, `httpd:alpine`).
- Les applis d'exemple sont **minimales et jetables** : un JAR « faux Spring Boot »
  écrit en 20 lignes, un `index.html` pour Angular. On simule la forme, pas le contenu.

## 5. Progression des labos

Chaque labo suppose acquis tout ce qui précède. Ordre non négociable.

| # | Dossier | Concept central | Points clés |
|---|---------|-----------------|-------------|
| 01 | `01-conteneurs-et-architecture` | Qu'est-ce qu'un conteneur | VM vs conteneur, namespaces & cgroups, architecture client/daemon/registry, image vs conteneur, anatomie de la CLI |
| 02 | `02-images-et-registries` | Les images | tags, digests, layers, cache, Docker Hub, `pull/images/inspect/history/rmi`, `save/load`, prune |
| 03 | `03-cycle-de-vie-conteneurs` | Faire tourner un conteneur | `run/ps/logs/exec/stop/kill/rm`, foreground vs detached, PID 1 et signaux, codes de sortie, restart policies |
| 04 | `04-dockerfile` | Construire une image | build context, instructions, `CMD` vs `ENTRYPOINT`, `ARG` vs `ENV`, `.dockerignore`, cache de build et ordre des couches |
| 05 | `05-multistage-et-optimisation` | Images de qualité prod | multi-stage (Maven→JRE, Node→nginx), taille, image de base, `USER` non-root, BuildKit |
| 06 | `06-donnees-et-volumes` | Persistance | couche writable, volumes nommés, bind mounts, tmpfs, permissions/UID, sauvegarde/restauration |
| 07 | `07-reseau` | Communication | bridge par défaut vs réseau *user-defined*, DNS interne, `-p` vs `EXPOSE`, host/none, chaîne Angular → Spring Boot → Postgres |
| 08 | `08-configuration-et-secrets` | Paramétrer sans rebuild | 12-factor, `-e` / `--env-file`, `ENV` vs `ARG`, profils Spring via variables, pourquoi un secret ne va jamais dans une image |
| 09 | `09-docker-compose` | Orchestrer la stack | `compose.yaml`, services/networks/volumes, `depends_on` + `healthcheck`, `up/down/logs/exec`, override par environnement |
| 10 | `10-exploitation-et-bonnes-pratiques` | Vivre avec Docker | `logs/inspect/stats/events`, HEALTHCHECK, limites CPU/mémoire, stratégie de tags, registry privé, sécurité de base, place dans une CI/CD |

## 6. Fil rouge « entreprise »

La même stack fictive traverse la série, en restant triviale :

- **`web`** — Angular *buildé* servi par nginx (en pratique : un `index.html` statique).
- **`api`** — Spring Boot (en pratique : un JAR minimal ou un simple serveur HTTP) qui
  écoute sur `8080`, lit sa config dans des variables d'environnement, expose
  `/actuator/health`.
- **`db`** — PostgreSQL officiel, avec volume nommé.

Elle apparaît par morceaux dès le labo 04 et est complète au labo 09. Aucun labo ne doit
exiger de compiler un vrai projet Maven ou npm : trop lent, hors sujet.

## 7. Contraintes de la machine de l'apprenant (vérifiées)

- **Docker Engine 29.x sur Linux natif**, daemon accessible sans `sudo`.
- **D'autres stacks tournent sur cette machine** (une stack Supabase, entre autres). Donc :
  **aucun labo ne doit proposer `docker system prune`, `docker image prune -a`,
  `docker container prune` ni `docker volume prune` sans réserve.** Le nettoyage se fait
  **nommément** (`docker rm -f <noms>`), ou avec un `--filter` explicite. Le sujet
  `prune` est traité au labo 10, avec les avertissements qui vont avec.
- **Docker 29 a supprimé le champ `.NetworkSettings.IPAddress`** de premier niveau dans
  `docker inspect`. Utiliser `.NetworkSettings.Networks.<réseau>.IPAddress`. Vérifier de
  la même façon tout champ de `inspect` avant de l'écrire dans un labo.
- **Le magasin d'images est celui de containerd** (`docker info` → `Storage Driver:
  overlayfs`, `driver-type: io.containerd.snapshotter.v1`). Deux conséquences pour les
  labos :
  - `docker images` n'affiche **plus** les colonnes `REPOSITORY / TAG / SIZE` mais
    `IMAGE / ID / DISK USAGE / CONTENT SIZE / EXTRA`. Pour retrouver la présentation
    classique des tutoriels : `docker images --format 'table {{.Repository}}\t{{.Tag}}\t
    {{.ID}}\t{{.Size}}'`. Toujours montrer les deux dans les labos.
  - Les **images *dangling*** n'apparaissent quasiment plus après une reconstruction sur
    le même tag (`--filter dangling=true` renvoie souvent vide). Ne pas bâtir d'exercice
    qui repose sur leur apparition ; les expliquer comme un concept, avec la réserve.
- Toute commande écrite dans un `04-labo-pratique.md` doit avoir été **exécutée** ici, et
  les sorties citées dans le texte doivent être les sorties réelles (tailles, statuts,
  messages d'erreur).

## 8. Checklist avant de considérer un labo terminé

- [ ] Les 4 `.md` existent et respectent le plan de la section 4.
- [ ] Les 4 `.pdf` sont générés et `01-theorie.pdf` fait ≤ 5 pages.
- [ ] Chaque question du `02` a sa réponse détaillée dans le `03`, même numérotation.
- [ ] Toutes les commandes du `04` ont été **exécutées réellement** et fonctionnent
      (images publiques disponibles, options valides pour Docker Engine ≥ 24).
- [ ] Les fichiers de `files/` sont présents et cohérents avec le texte du labo.
- [ ] Section « Nettoyage » présente à la fin du labo pratique.
- [ ] Le `README.md` liste le labo.
