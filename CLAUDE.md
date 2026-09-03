# CLAUDE.md — Série de labos Docker (CLI), pratiqués avec Podman sur WSL

Ce dépôt contient une série de labos d'auto-formation Docker, orientés **ligne de
commande**, en **trois langues** (FR, NL-BE, EN). Objectif final : comprendre Docker tel
qu'il est utilisé en entreprise sur une stack **Spring Boot + Angular + PostgreSQL**, tout
en gardant chaque labo **simple et centré sur les conteneurs** (jamais sur Java, ni sur
TypeScript). **Le moteur utilisé en pratique est Podman (rootless) dans une distribution
Ubuntu sous WSL 2** ; la théorie enseigne le vocabulaire Docker et explique à chaque fois
ce que Podman fait différemment.

---

## 1. Public et objectif

- **Apprenant** : développeur qui connaît le terminal Linux, découvre Docker, travaille
  sur un poste Windows avec WSL 2 + Ubuntu + `apt install podman`.
- **But** : maîtriser les concepts fondamentaux + le vocabulaire employé en entreprise,
  avec Podman comme moteur (CLI identique à Docker).
- **Non-but** : apprendre Kubernetes, Swarm, Java ou Angular. On y fait référence, on ne
  les enseigne pas.
- **Ton** : les pages de théorie doivent être **intéressantes** — un fil narratif, une
  anecdote historique (Docker 2013, OCI 2015, Podman 2018, WSL 2…), des « pourquoi »,
  pas une documentation de référence.

## 2. Format imposé (à respecter pour CHAQUE labo)

Chaque labo existe en **trois langues** — `fr/` (français), `nl/` (néerlandais de
Belgique), `en/` (anglais) — et chaque langue produit **4 PDF**, générés à partir de
4 fichiers Markdown (noms de fichiers traduits, numérotation identique) :

| FR | NL | EN | Rôle |
|----|----|----|------|
| `01-theorie.md` | `01-theorie.md` | `01-theory.md` | Cours théorique. **5 pages max.** Commandes en illustration, **pas d'exercice**. |
| `02-questions.md` | `02-vragen.md` | `02-questions.md` | Questions de contrôle. **Pas faciles** : compréhension, pas mémorisation. |
| `03-reponses.md` | `03-antwoorden.md` | `03-answers.md` | Corrigé : réponse + mécanisme + nuance + exemple vérifiable. |
| `04-labo-pratique.md` | `04-praktijklabo.md` | `04-hands-on-lab.md` | Manipulation guidée au terminal, sorties réelles. |

**Le français est la version maîtresse** : on écrit et on valide en FR, puis on produit
les versions NL et EN. Les termes techniques sans bon équivalent restent en anglais dans
les trois langues (*image*, *layer*, *registry*, *bind mount*, *build context*,
*rootless*, *digest*…).

### Règles de traduction NL/EN

**On traduit le sens, jamais la phrase.** Une version NL ou EN doit se lire comme si elle
avait été écrite nativement dans cette langue. Test final obligatoire avant de générer les
PDF : relire le document NL/EN **sans** le FR à côté ; si la phrase française se devine
sous la traduction (ordre des mots, ponctuation, images), on réécrit le passage.

- **Reste identique au FR** : la structure et la numérotation des sections, les tableaux,
  les étiquettes d'encadrés (via leurs équivalents convenus, section 3), les commandes
  (mêmes outils, mêmes options, même ordre) et les **sorties réelles des outils**
  (messages d'erreur, tailles, statuts — produits en anglais par les outils, ils restent
  tels quels dans les trois langues).
- **Est localisé** : ce que l'apprenant tape ou nomme lui-même — noms de conteneurs et de
  fichiers, chaînes des `echo`, commentaires pédagogiques (`veilleur` → `waker` / `watcher`,
  `notes.txt` → `notes.txt`/`notities.txt` selon la langue…).
- **S'adapte librement** : le découpage des phrases (casser les phrases françaises à
  deux-points et tirets cadratins en deux ou trois phrases courtes), l'ordre des mots, les
  métaphores, anecdotes et traits d'esprit (trouver l'équivalent naturel de la langue
  cible, ou supprimer — ne jamais transposer mot à mot), l'emphase (le « **LE** canal » à
  la française ne devient jamais `HET`/`THE` en capitales : on reformule, p. ex. *the one
  configuration channel that matters*).
- **EN** : style *technical writing* — phrases sujet-verbe-complément directes, verbes
  forts, voix active ; pas de phrases nominales, d'appositions en tête de phrase ni
  d'inversions rhétoriques ; les récits historiques au prétérit, jamais au présent
  historique.
- **NL** : néerlandais standard naturel, lisible en Belgique — tutoiement « je », phrases
  courtes, ordre des mots naturel, pas de flandricismes gratuits ni de tournures calquées
  du français.
- **Faux amis interdits** (déjà rencontrés — la liste s'allonge au besoin) :
  « ponctuellement » ne se traduit **jamais** par `punctueel` (NL) ni `punctually` (EN)
  — ces mots signifient « à l'heure » ; dire `waar nodig` / `alleen wanneer het nodig is`,
  `when needed` / `case by case`. « Sans appel » ≠ `without appeal` (dire `no reprieve`,
  `final`). « Interlocuteur » ≠ `interlocutor` (dire `no one to talk to`). « Grille de
  lecture » ≠ `reading grid` (dire `mental model`, `frame`).

Plus, si nécessaire :

- `files/` : fichiers de base fournis pour le labo pratique (Dockerfile, compose,
  sources minimales…), **communs aux trois langues** (commentaires en français simple ou
  neutres). Quand la création du fichier **est** l'exercice, le labo demande à
  l'apprenant de l'écrire ; sinon le fichier est fourni ici, prêt à l'emploi.

### Arborescence

```
docker-lab/
├── CLAUDE.md
├── README.md                  # sommaire + mode d'emploi
├── build.sh                   # génère tous les PDF
├── tools/build_pdf.py         # Markdown -> HTML -> PDF (Chrome headless), encadrés typés
├── tools/podman-sandbox.sh    # Podman rootless de test dans un conteneur Docker privilégié
├── assets/pdf.css             # mise en page des PDF
└── labs/
    ├── 01-conteneurs-et-architecture/
    │   ├── fr/  01-theorie.md 02-questions.md 03-reponses.md 04-labo-pratique.md (+ .pdf)
    │   ├── nl/  01-theorie.md 02-vragen.md 03-antwoorden.md 04-praktijklabo.md   (+ .pdf)
    │   ├── en/  01-theory.md 02-questions.md 03-answers.md 04-hands-on-lab.md    (+ .pdf)
    │   └── files/
    └── ...
```

## 3. Chaîne de génération des PDF

```bash
./build.sh                 # tout reconstruire
./build.sh labs/03-*       # reconstruire un labo (trois langues)
./build.sh labs/03-*/nl    # une seule langue
```

- `build.sh` crée `.venv/` au besoin (`markdown`, `pygments`) puis lance
  `tools/build_pdf.py`.
- Conversion : Markdown → HTML (extensions `fenced_code`, `tables`, `attr_list`,
  `sane_lists`, `codehilite`) → PDF via `google-chrome --headless --print-to-pdf`.
- **Ne jamais éditer un `.pdf` à la main** : il est régénéré. La source de vérité est le
  `.md`.
- Après génération, **vérifier le nombre de pages** de chaque `01-*.pdf` (le script
  l'affiche et marque `TROP LONG`). S'il dépasse 5, raccourcir le Markdown — pas la CSS.
  `pdftotext -f 6 -l 6 fichier.pdf -` montre ce qui déborde. Un texte FR de ~1700 mots
  hors code tient ; les traductions NL/EN doivent être vérifiées séparément.

### Conventions Markdown utilisées par le gabarit

- `# Titre` : titre du document (une seule fois, en tête).
- `## Section` : commence **toujours** une nouvelle section ; pas de saut de page forcé
  sauf `<div class="page-break"></div>`.
- Blocs de code : toujours annotés (` ```bash `, ` ```dockerfile `, ` ```yaml `).
- Encadrés : une citation dont la première ligne commence par une **étiquette en gras
  suivie d'un tiret cadratin** (`> **Étiquette** — …`) devient un encadré typé
  (`tools/build_pdf.py`, `assets/pdf.css`) :
  - `À retenir` / `Onthouden` / `Remember` → encadré bleu (point clé) ;
  - `Piège` / `Valkuil` / `Pitfall` → encadré orange (erreur classique) ;
  - `Podman` → encadré violet : ce que Podman fait différemment de Docker ;
  - **toute autre étiquette** → encadré vert « domaine », avec l'étiquette affichée en
    petit label : `Linux`, `Java`, `Réseau` / `Netwerk` / `Network`, `Windows / WSL`,
    `Sécurité` / `Beveiliging` / `Security`, `Histoire` / `Geschiedenis` / `History`,
    `Spring Boot`, `Angular`, `HTTP`, `Linux / Shell`… **Chaque fois que la théorie
    s'appuie sur une notion extérieure aux conteneurs, on l'explique en 3-5 lignes dans
    un tel encadré**, plutôt que de supposer qu'elle est connue.
  - Un encadré = un seul paragraphe. Deux à cinq encadrés par page de théorie, pas plus.
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
- **Podman à chaque labo** : au moins un encadré `Podman` (pas de daemon, rootless,
  `conmon`, noms complets, `--tls-verify`, Buildah, Quadlet, pods…) et, quand une
  commande ou une sortie diffère de Docker, le dire — sans transformer le cours en
  comparatif. On enseigne Docker, on pratique Podman.
- 5 pages A4 = environ 1500-1800 mots hors blocs de code, encadrés compris.

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
- Tout doit tourner dans **une distribution Ubuntu sous WSL 2 avec Podman rootless**
  (`apt install podman`, `systemd=true` dans `/etc/wsl.conf`), sans compte payant, sans
  cloud, avec des images publiques légères (`alpine`, `nginx:alpine`,
  `postgres:16-alpine`, `eclipse-temurin`, `node:22-alpine`, `registry:2`).
- Les commandes s'écrivent `podman …` ; les noms d'images dans les Dockerfiles et les
  scripts sont **complets** (`docker.io/library/…`) ; les noms courts à alias
  (`alpine`, `nginx`, `debian`, `postgres`, `registry`, `node`) sont tolérés en ligne de
  commande. Les nettoyages utilisent `podman rm -f -t 0` (sinon 10 s d'attente).
- Ce qui est propre à WSL (kernel `-microsoft-standard-WSL2`, `localhost` forwarding vers
  Windows, `.wslconfig`, `wsl --shutdown`) est signalé dans un encadré `Windows / WSL`.
- Les applis d'exemple sont **minimales et jetables** : un JAR « faux Spring Boot »
  écrit en 20 lignes, un `index.html` pour Angular. On simule la forme, pas le contenu.

## 5. Progression des labos

Chaque labo suppose acquis tout ce qui précède. Ordre non négociable.

| # | Dossier | Concept central | Points clés |
|---|---------|-----------------|-------------|
| 00 | `00-fondamentaux-linux` | Les fondamentaux Linux prérequis | noyau vs userland, processus (PID, signaux, codes de sortie), UID/GID et permissions, montages et `/proc`, variables d'environnement et `PATH`, redirections/pipes, ports et `localhost`. **Aucun conteneur** : tourne sur Ubuntu 24.04/WSL nu, sans Podman ni installation |
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

## 7. Contraintes des machines (vérifiées)

**Machine de l'apprenant (cible des labos)** : Windows + WSL 2 + Ubuntu + Podman ≥ 4.9
rootless (sorties de référence produites avec Podman 5.8). Conséquences :

- **Pas de daemon** : `podman version` n'a qu'un bloc `Client` ; `--restart` ne survit
  pas à `wsl --shutdown` ; `podman rm -f` attend 10 s sans `-t 0` ; `stop` affiche
  `StopSignal SIGTERM failed … resorting to SIGKILL`.
- **Rootless** : `root` du conteneur = UID de l'utilisateur (`podman top … user,huser`,
  `podman unshare cat /proc/self/uid_map`) ; ports < 1024 refusés (`pasta failed …
  Permission denied`) ; réseau par défaut `pasta` → `.NetworkSettings.IPAddress` **vide**
  (utiliser `--network podman` pour obtenir `10.88.0.x`) ; `--memory` et `podman stats`
  exigent la délégation cgroup v2 par systemd.
- **Images** : `podman images` affiche les colonnes classiques `REPOSITORY/TAG/IMAGE ID/
  SIZE`, les noms **complets** (`docker.io/library/…`, `localhost/…`), et les images
  *dangling* apparaissent bien après un rebuild sur le même tag. Les tailles diffèrent
  de Docker (non compressées) : `alpine` 8.7 MB, `nginx:alpine` 64.2 MB,
  `eclipse-temurin:21-jre-alpine` 209 MB, `21-jdk` 488 MB, `node:22-alpine` 167 MB.
- **Registry local** : `podman push localhost:5000/...` échoue sans `--tls-verify=false`
  (`http: server gave HTTP response to HTTPS client`).
- **Build** : sortie `STEP x/y`, `--> Using cache`, `[1/2] STEP …` en multi-stage, pas
  de ligne `transferring context`, `# syntax=` ignoré, `--mount=type=cache|secret`
  supportés, `--target`, `--build-context`.
- **Nettoyage** : jamais `podman system prune`, `image prune -a`, `container prune` ni
  `volume prune` sans réserve dans un labo ; on supprime **nommément**. `prune` est
  traité au labo 10 avec les avertissements.

**Machine de rédaction (celle-ci)** : Ubuntu natif avec Docker Engine 29, **sans Podman
installé et sans `sudo`**. Pour exécuter réellement les commandes, utiliser
`tools/podman-sandbox.sh` (Podman 5.8 rootless dans un conteneur Docker privilégié,
cgroups délégués, `unqualified-search-registries = ["docker.io"]`,
`ip_unprivileged_port_start=1024`). Ce que le bac à sable **ne** reproduit **pas** :
le noyau WSL (`uname -r` donne celui de l'hôte), `systemd` (cgroupManager = `cgroupfs`),
la plage `/etc/subuid` d'Ubuntu (`100000:65536` — le bac à sable a `1001:64535`, donc
`HUSER` d'un UID 1000 vaut `100999` sur WSL mais `1001` dans le bac à sable), Quadlet.
Ces valeurs sont écrites « telles que sur WSL » dans les labos et signalées comme telles.

- Toute commande écrite dans un `04-*.md` doit avoir été **exécutée** dans le bac à
  sable (ou sur un vrai WSL), et les sorties citées doivent être les sorties réelles
  (tailles, statuts, messages d'erreur).

## 8. Checklist avant de considérer un labo terminé

- [ ] Les 4 `.md` existent **dans les trois langues** (`fr/`, `nl/`, `en/`) et
      respectent le plan de la section 4.
- [ ] Les 12 `.pdf` sont générés et chaque `01-*.pdf` fait ≤ 5 pages (dans les trois
      langues).
- [ ] Chaque question du `02` a sa réponse détaillée dans le `03`, même numérotation.
- [ ] La théorie contient au moins un encadré `Podman` et des encadrés « domaine » pour
      chaque notion extérieure aux conteneurs.
- [ ] Toutes les commandes du `04` ont été **exécutées réellement** (bac à sable ou WSL)
      et fonctionnent avec Podman ≥ 4.9 rootless.
- [ ] Les fichiers de `files/` sont présents et cohérents avec le texte du labo.
- [ ] Section « Nettoyage » présente à la fin du labo pratique, avec `rm -f -t 0`.
- [ ] Le `README.md` liste le labo.
