# CLAUDE.md — Série de labos Docker puis Kubernetes (CLI), pratiqués sur WSL

Ce dépôt contient une série de labos d'auto-formation orientés **ligne de commande**, en
**trois langues** (FR, NL-BE, EN), en **deux parties** :

- **Partie 1 — Docker (labos 00 à 10)** : après un labo 00 de fondamentaux Linux
  (sans conteneur), comprendre Docker tel qu'il est utilisé en
  entreprise sur une stack **Spring Boot + Angular + PostgreSQL**, en pratiquant avec
  **Podman (rootless) dans une distribution Ubuntu sous WSL 2**. La théorie enseigne le
  vocabulaire Docker et explique à chaque fois ce que Podman fait différemment.
- **Partie 2 — Kubernetes (labos 11 à 17)** : une fois les conteneurs maîtrisés,
  déployer la même stack sur un cluster Kubernetes, en pratiquant avec **k3s** (un
  Kubernetes certifié, mono-nœud, installé dans la même Ubuntu/WSL). La théorie
  enseigne le vocabulaire Kubernetes « standard » et explique à chaque fois ce que k3s
  fait différemment d'un cluster d'entreprise (managé ou non).

Chaque labo reste **simple et centré sur les conteneurs / le cluster** (jamais sur Java,
ni sur TypeScript).

---

## 1. Public et objectif

- **Apprenant** : développeur qui connaît le terminal Linux, découvre Docker puis
  Kubernetes, travaille sur un poste Windows avec WSL 2 + Ubuntu (`sudo` disponible),
  `apt install podman`, puis k3s (labo 11).
- **But partie 1** : maîtriser les concepts fondamentaux des conteneurs + le vocabulaire
  employé en entreprise, avec Podman comme moteur (CLI identique à Docker).
- **But partie 2** : être capable de **lire, écrire et déboguer** les manifestes
  Kubernetes d'une application d'entreprise (Deployment, Service, Ingress, ConfigMap,
  Secret, PVC, StatefulSet, Helm chart) et de dialoguer avec une équipe « ops » : pas
  d'administrer un cluster.
- **Non-but** : apprendre Swarm, Java ou Angular. Pas de préparation à une
  certification (CKA/CKAD), pas d'installation multi-nœuds, pas de cloud. On y fait
  référence, on ne les enseigne pas.
- **Ton** : les pages de théorie doivent être **intéressantes** — un fil narratif, une
  anecdote historique (Docker 2013, Kubernetes/Borg 2014, OCI 2015, Podman 2018,
  k3s 2019, WSL 2…), des « pourquoi », pas une documentation de référence.

## 2. Format imposé (à respecter pour CHAQUE labo, Docker comme Kubernetes)

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
*rootless*, *digest*, *pod*, *deployment*, *service*, *ingress*, *namespace*,
*rolling update*…).

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

### Calques de l'anglais interdits — en FR **et** en NL

La documentation source (Docker, Podman, Kubernetes) est en anglais : le risque n'est
pas seulement de calquer le FR en NL/EN, mais de calquer **l'anglais dans le FR** (et
dans le NL). Le FR, version maîtresse, doit lui aussi se lire comme écrit nativement :
on garde le **jargon** en anglais (*layer*, *registry*, *pod*…), jamais la **syntaxe**
ni les faux amis anglais.

- **FR** — interdits : *supporter* au sens de prendre en charge (dire « prend en
  charge », « gère »), *librairie* (« bibliothèque »), *digital* (« numérique »),
  *adresser un problème* (« traiter »), *faire du sens* (« avoir du sens »),
  *versatile* (« polyvalent »), *confusant* (« déroutant »), *assumer que*
  (« supposer que »), *opportunité* (« occasion »), *délivrer* (« livrer »),
  *initier* (« lancer »), *dramatique* (« spectaculaire »), *au final*, *en charge de*,
  et les verbes franglais (*checker*, *monitorer*, *updater*, *forwarder*, *setter*,
  *customiser*). Faux amis à relire en contexte : *actually* ≠ « actuellement »,
  *eventually* ≠ « éventuellement », *definitely* ≠ « définitivement », *globally* ≠
  « globalement ». Pas de structures anglaises : « il est possible de », « dans le but
  de », nominalisations en chaîne, *passif* systématique.
- **NL** — interdits : *supporteren* (« ondersteunen »), *zin maken* (« logisch
  zijn »), *adresseren* (« aanpakken »), *runnen* hors commande (« draaien »),
  *checken* (« nagaan »), *dedicated* (« specifiek », « eigen »), *best practices* en
  prose (« goede gewoonten » ou en italique comme terme). Faux amis : *actueel* ≠
  *actually* (« eigenlijk »), *eventueel* ≠ *eventually* (« uiteindelijk »). Et les
  gallicismes belges : *in functie van* (« afhankelijk van »), *op het niveau van*,
  *ter hoogte van*, *op het einde* (« aan het einde »), *werkpost*, *verwittigen*,
  *noteer dat* (« merk op dat »), *men* pour « on » (dire « je »).
- **Vérification** : `python3 tools/lint_lang.py [labs/NN-*]` repère ces calques dans
  la prose (hors blocs de code) et échoue s'il en trouve ; `--all` affiche aussi les
  faux amis « à relire en contexte ». Le script n'est qu'un filet : la relecture de
  chaque langue **sans la source à côté** reste obligatoire, et **tout calque repéré en
  relecture est ajouté aux listes du script** (et à cette section).

Plus, si nécessaire :

- `files/` : fichiers de base fournis pour le labo pratique (Dockerfile, compose,
  manifestes YAML, chart Helm, sources minimales…), **communs aux trois langues**
  (commentaires en français simple ou neutres). Quand la création du fichier **est**
  l'exercice, le labo demande à l'apprenant de l'écrire ; sinon le fichier est fourni
  ici, prêt à l'emploi.

### Arborescence

```
docker-lab/
├── CLAUDE.md
├── README.md                  # sommaire + mode d'emploi
├── build.sh                   # génère tous les PDF
├── tools/build_pdf.py         # Markdown -> HTML -> PDF (Chrome headless), encadrés typés
├── tools/lint_lang.py         # repère les calques et faux amis FR/NL/EN dans la prose
├── tools/podman-sandbox.sh    # Podman rootless de test dans un conteneur Docker privilégié
├── tools/k3s-sandbox.sh       # k3s de test dans un conteneur Docker privilégié (à créer au labo 11)
├── assets/pdf.css             # mise en page des PDF
└── labs/
    ├── 01-conteneurs-et-architecture/
    │   ├── fr/  01-theorie.md 02-questions.md 03-reponses.md 04-labo-pratique.md (+ .pdf)
    │   ├── nl/  01-theorie.md 02-vragen.md 03-antwoorden.md 04-praktijklabo.md   (+ .pdf)
    │   ├── en/  01-theory.md 02-questions.md 03-answers.md 04-hands-on-lab.md    (+ .pdf)
    │   └── files/
    ├── ...
    ├── 10-exploitation-et-bonnes-pratiques/
    ├── 11-pourquoi-kubernetes/            # début de la partie Kubernetes
    │   ├── fr/ nl/ en/
    │   └── files/   # manifestes YAML
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
  - `k3s` → encadré violet (même style) : ce que k3s fait différemment d'un cluster
    Kubernetes d'entreprise (EKS/AKS/GKE, OpenShift, kubeadm) ;
  - **toute autre étiquette** → encadré vert « domaine », avec l'étiquette affichée en
    petit label : `Linux`, `Java`, `Réseau` / `Netwerk` / `Network`, `Windows / WSL`,
    `Sécurité` / `Beveiliging` / `Security`, `Histoire` / `Geschiedenis` / `History`,
    `Spring Boot`, `Angular`, `HTTP`, `Linux / Shell`, `YAML`, `Rappel Docker` /
    `Docker-herhaling` / `Docker recap`… **Chaque fois que la théorie s'appuie sur une
    notion extérieure au sujet du labo, on l'explique en 3-5 lignes dans un tel
    encadré**, plutôt que de supposer qu'elle est connue.
  - Un encadré = un seul paragraphe. Deux à cinq encadrés par page de théorie, pas plus.
- Tableaux : privilégiés pour les comparaisons (commande / effet / quand l'utiliser).

## 4. Règles de rédaction

**Théorie**
- Français clair, phrases courtes. Le jargon anglais reste en anglais (*image*, *layer*,
  *registry*, *bind mount*, *pod*, *deployment*…) avec la traduction à la première
  occurrence.
- Chaque document commence par « Objectifs » (3-5 puces) et finit par « À retenir »
  (5-7 puces) + « Vocabulaire ».
- Toujours expliquer le **pourquoi**, pas seulement le comment.
- Un lien explicite avec l'entreprise dans une courte section « En entreprise » :
  comment ce concept se traduit sur une stack Spring Boot / Angular.
- **Partie Docker — Podman à chaque labo** : au moins un encadré `Podman` (pas de
  daemon, rootless, `conmon`, noms complets, `--tls-verify`, Buildah, Quadlet, pods…)
  et, quand une commande ou une sortie diffère de Docker, le dire — sans transformer le
  cours en comparatif. On enseigne Docker, on pratique Podman.
- **Partie Kubernetes — k3s à chaque labo** : au moins un encadré `k3s` (binaire
  unique, containerd embarqué, Traefik comme Ingress controller, ServiceLB,
  StorageClass `local-path`, `kubectl` fourni, SQLite au lieu d'etcd…) et au moins un
  encadré `Rappel Docker` qui relie la notion au labo Docker correspondant (probe ↔
  `HEALTHCHECK`, ConfigMap ↔ `--env-file`, PVC ↔ volume nommé, Service ↔ DNS du réseau
  user-defined, Helm ↔ Compose…). On enseigne Kubernetes, on pratique k3s. Un encadré
  `Podman` reste bienvenu quand Podman intervient (`podman generate kube`,
  `podman kube play`, export d'image vers le cluster).
- 5 pages A4 = environ 1500-1800 mots hors blocs de code, encadrés compris. Les
  manifestes YAML comptent comme blocs de code : les garder **minimaux** (pas de champs
  optionnels « au cas où »).

**Questions**
- 10 à 14 questions, numérotées, difficulté croissante.
- Types imposés : questions de raisonnement (« que se passe-t-il si… »), de diagnostic
  (« voici une sortie de commande / un Dockerfile / un manifeste, qu'est-ce qui
  cloche ? »), de comparaison (« X vs Y, dans quel cas… »), et de prédiction de
  résultat.
- **Interdit** : questions dont la réponse est un mot recopié du cours, QCM triviaux.
- Indiquer entre crochets le niveau : `[Compréhension]`, `[Analyse]`, `[Diagnostic]`.

**Réponses**
- Pour chaque question : **Réponse** (courte et nette) → **Pourquoi** (le mécanisme) →
  **Nuance / piège** → **Exemple** (commande, sortie ou extrait de fichier).
- Ne jamais se contenter d'affirmer : montrer la commande qui prouve la réponse.

**Labo pratique (commun)**
- Étapes numérotées, chacune avec : la ou les commandes, ce qu'on doit observer, et une
  phrase d'explication.
- Toujours terminer par une section « Nettoyage » pour ne pas laisser la machine
  encombrée.
- Tout doit tourner dans **une distribution Ubuntu sous WSL 2** (`systemd=true` dans
  `/etc/wsl.conf`), sans compte payant, sans cloud, avec des images publiques légères
  (`alpine`, `nginx:alpine`, `postgres:16-alpine`, `eclipse-temurin`, `node:22-alpine`,
  `registry:2`).
- Ce qui est propre à WSL (kernel `-microsoft-standard-WSL2`, `localhost` forwarding vers
  Windows, `.wslconfig`, `wsl --shutdown`) est signalé dans un encadré `Windows / WSL`.
- Les applis d'exemple sont **minimales et jetables** : un JAR « faux Spring Boot »
  écrit en 20 lignes, un `index.html` pour Angular. On simule la forme, pas le contenu.

**Labo pratique — partie Docker (01-10)**
- Les commandes s'écrivent `podman …` ; les noms d'images dans les Dockerfiles et les
  scripts sont **complets** (`docker.io/library/…`) ; les noms courts à alias
  (`alpine`, `nginx`, `debian`, `postgres`, `registry`, `node`) sont tolérés en ligne de
  commande. Les nettoyages utilisent `podman rm -f -t 0` (sinon 10 s d'attente) et
  `podman rmi` nommément.

**Labo pratique — partie Kubernetes (11-17)**
- Les commandes s'écrivent `kubectl …` (celui fourni par k3s). Les images utilisées
  par les manifestes sont soit publiques avec nom complet (`docker.io/library/…`), soit
  construites avec Podman dans la partie 1 et **importées dans le cluster** :
  `podman save localhost/api:1.0 | sudo k3s ctr images import -`, avec
  `imagePullPolicy: IfNotPresent` (ou `Never`) dans le manifeste.
- Chaque labo travaille dans **son propre namespace** `labNN` (créé à l'étape 1,
  positionné avec `kubectl config set-context --current --namespace=labNN`) ; le
  nettoyage = `kubectl delete namespace labNN` + retour au namespace `default`, et
  suppression des images importées si le labo en a importé. Les ressources
  *cluster-scoped* créées (StorageClass, ClusterRole…) sont supprimées nommément.
- Les manifestes sont fournis dans `files/` sauf quand les écrire **est** l'exercice.
  Un manifeste par fichier, nommé `<kind>-<nom>.yaml` (`deployment-api.yaml`), ou un
  seul fichier `stack.yaml` séparé par `---` quand le labo déploie toute la stack.
- Les sorties `kubectl get` sont citées avec les colonnes réelles ; les valeurs
  variables (AGE, IP de pod, suffixes de ReplicaSet `-7d9f8b6c5`) sont laissées telles
  quelles, avec une phrase disant qu'elles diffèrent chez l'apprenant.

## 5. Progression des labos

Chaque labo suppose acquis tout ce qui précède. Ordre non négociable. La partie
Kubernetes ne commence qu'une fois la partie Docker **entièrement terminée** (les onze
labos 00-10, trois langues).

### Partie 1 — Docker (pratiqué avec Podman)

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

### Partie 2 — Kubernetes (pratiqué avec k3s)

| # | Dossier | Concept central | Points clés |
|---|---------|-----------------|-------------|
| 11 | `11-pourquoi-kubernetes` | Du Compose au cluster | limites de Compose (une machine, pas d'auto-réparation, pas de scaling), ce qu'est un *cluster*, control plane (API server, etcd, scheduler, controller manager) vs nœuds (kubelet, containerd, kube-proxy), **modèle déclaratif et boucle de réconciliation**, installation de k3s sur WSL, `kubectl get/describe/apply/delete`, premier Pod, passerelle Podman (`podman generate kube`, `podman kube play`) |
| 12 | `12-pods-deployments-et-probes` | Faire tourner et mettre à jour | Pod (un ou plusieurs conteneurs, réseau et volumes partagés, éphémère), labels & selectors, ReplicaSet, Deployment, `scale`, rolling update et `rollout undo`, `logs/exec/port-forward`, probes liveness/readiness/startup (↔ `HEALTHCHECK`), importer une image Podman dans k3s, `imagePullPolicy` |
| 13 | `13-services-et-ingress` | Exposer | Service ClusterIP/NodePort/LoadBalancer, Endpoints, CoreDNS et noms `svc.cluster.local`, Ingress et Ingress controller (Traefik dans k3s), chaîne web → api, comparaison avec `-p` et le DNS Compose |
| 14 | `14-configmaps-et-secrets` | Paramétrer sans rebuild | ConfigMap, Secret (base64 **n'est pas** du chiffrement), `env`/`envFrom` vs fichiers montés, profils Spring, redéploiement après changement de config, secrets externes (Vault, Sealed Secrets) mentionnés |
| 15 | `15-stockage-et-statefulsets` | Persister | PersistentVolume, PersistentVolumeClaim, StorageClass (`local-path` dans k3s), modes d'accès, StatefulSet pour Postgres, headless Service, identité stable, sauvegarde/restauration |
| 16 | `16-ressources-et-exploitation` | Vivre avec un cluster | namespaces et contextes, requests/limits, classes QoS, `OOMKilled`, `kubectl top`, events, diagnostic (`Pending`, `CrashLoopBackOff`, `ImagePullBackOff`), RBAC de base (ServiceAccount/Role/RoleBinding), NetworkPolicy mentionnée |
| 17 | `17-helm-et-livraison` | Packager et livrer | Helm (chart, `values.yaml`, release, `install/upgrade/rollback`), Kustomize (overlays par environnement), stratégie de tags et digests, pipeline CI/CD → cluster, GitOps (Argo CD) mentionné, k3s vs clusters managés (EKS/AKS/GKE) et OpenShift |

## 6. Fil rouge « entreprise »

La même stack fictive traverse la série, en restant triviale :

- **`web`** — Angular *buildé* servi par nginx (en pratique : un `index.html` statique).
- **`api`** — Spring Boot (en pratique : un JAR minimal ou un simple serveur HTTP) qui
  écoute sur `8080`, lit sa config dans des variables d'environnement, expose
  `/actuator/health`.
- **`db`** — PostgreSQL officiel, avec volume nommé.

Elle apparaît par morceaux dès le labo 04 et est complète au labo 09 (Compose). La
partie Kubernetes la **redéploie morceau par morceau** avec les mêmes images :
`api` en Deployment + probes (12), `web` → `api` via Services + Ingress (13), config et
mot de passe de `db` en ConfigMap/Secret (14), `db` en StatefulSet + PVC (15), limites
et namespace dédié (16), le tout packagé en chart Helm (17). Aucun labo ne doit exiger
de compiler un vrai projet Maven ou npm : trop lent, hors sujet.

## 7. Contraintes des machines (vérifiées)

### 7.1 Machine de l'apprenant — partie Docker

**Windows + WSL 2 + Ubuntu + Podman ≥ 4.9 rootless** (sorties de référence produites
avec Podman 5.8). Conséquences :

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

### 7.2 Machine de l'apprenant — partie Kubernetes

**La même Ubuntu/WSL + k3s** (version de référence : **v1.34.1+k3s1**, Kubernetes
1.34, containerd 2.1), installé au labo 11 par le script officiel :

```bash
curl -sfL https://get.k3s.io | sudo sh -s - --write-kubeconfig-mode 644
```

Pourquoi k3s et pas kind/minikube : un seul binaire, un service systemd (donc il
redémarre après `wsl --shutdown`), `kubectl` fourni (`/usr/local/bin/kubectl`), et
**Ingress (Traefik), LoadBalancer (ServiceLB) et StorageClass (`local-path`) inclus**
— les labos 13 et 15 n'ont rien à installer en plus. Et le **même binaire** tourne
dans un conteneur Docker sur la machine de rédaction, donc les sorties sont identiques.
Conséquences à signaler dans les labos :

- **Prérequis** : `systemd=true` dans `/etc/wsl.conf` (déjà exigé par la partie
  Docker), `sudo`, et au moins **4 Go de RAM pour WSL** (`.wslconfig`, `memory=6GB`
  recommandé). k3s tourne en **root** (c'est le kubelet) — ce n'est pas rootless comme
  Podman ; un encadré `Sécurité` l'explique au labo 11.
- **Deux runtimes côte à côte** : Podman (rootless, `~/.local/share/containers`) et le
  containerd de k3s (root, `/var/lib/rancher/k3s`) **ne partagent pas** leurs images.
  D'où `podman save … | sudo k3s ctr images import -` (ou un push vers le registry
  `localhost:5000` du labo 10 + `/etc/rancher/k3s/registries.yaml`, montré au labo 17).
  `sudo k3s crictl images` liste les images vues par le cluster.
- **Kubeconfig** : `/etc/rancher/k3s/k3s.yaml`, lisible grâce à
  `--write-kubeconfig-mode 644` ; `kubectl` de k3s le trouve seul. Si l'apprenant
  installe un autre `kubectl`/Helm/Lens : `export KUBECONFIG=/etc/rancher/k3s/k3s.yaml`.
- **Nom du nœud** = hostname de la machine (`kubectl get nodes` affiche le nom
  Windows en minuscules) ; les sorties de référence montrent `wsl-ubuntu` et le disent.
- **Composants k3s** visibles dans `kube-system` : `coredns`, `local-path-provisioner`,
  `metrics-server`, `traefik`, `svclb-traefik-…` ; `kubectl top` fonctionne sans rien
  installer (metrics-server inclus).
- **Accès depuis Windows** : un Service NodePort ou l'Ingress Traefik (port 80/443 du
  nœud) sont joignables sur `http://localhost:…` depuis le navigateur Windows grâce au
  forwarding WSL ; `kubectl port-forward` aussi (il écoute sur `127.0.0.1`).
- **Arrêt / reprise** : `wsl --shutdown` tue le cluster ; au redémarrage de la distro,
  systemd relance k3s et les Pods reviennent (contrairement à `--restart` Podman).
  `sudo systemctl stop k3s` pour l'arrêter proprement ; `/usr/local/bin/k3s-uninstall.sh`
  pour tout retirer (montré au nettoyage final du labo 17).
- **Nettoyage** : par namespace (`kubectl delete namespace labNN`), jamais
  `kubectl delete all --all -A`.

### 7.3 Machine de rédaction (celle-ci)

Ubuntu natif avec Docker Engine 29, **sans Podman, sans k3s et sans `sudo`**.

- **Partie Docker** : `tools/podman-sandbox.sh` (Podman 5.8 rootless dans un conteneur
  Docker privilégié, cgroups délégués, `unqualified-search-registries = ["docker.io"]`,
  `ip_unprivileged_port_start=1024`). Ce que le bac à sable **ne** reproduit **pas** :
  le noyau WSL (`uname -r` donne celui de l'hôte), `systemd` (cgroupManager =
  `cgroupfs`), la plage `/etc/subuid` d'Ubuntu (`100000:65536` — le bac à sable a
  `1001:64535`, donc `HUSER` d'un UID 1000 vaut `100999` sur WSL mais `1001` dans le
  bac à sable), Quadlet. Ces valeurs sont écrites « telles que sur WSL » dans les labos
  et signalées comme telles.
- **Partie Kubernetes** : `tools/k3s-sandbox.sh` (**à créer au début du labo 11**, sur
  le modèle de `podman-sandbox.sh`) : l'image `docker.io/rancher/k3s:v1.34.1-k3s1`
  lancée `--privileged --hostname wsl-ubuntu … server --write-kubeconfig-mode 644`,
  avec `up / run / shell / copy-labs / import-image / down`. Vérifié le 17/10/2026 :
  le nœud est `Ready` en moins de 30 s sur cette machine. `import-image` fait le pont
  avec le bac à sable Podman (`podman save` d'un côté, `k3s ctr images import -` de
  l'autre), exactement comme l'apprenant le fera sur WSL. Helm (labo 17) est téléchargé
  comme binaire dans le conteneur. Ce que ce bac à sable **ne** reproduit **pas** :
  `systemctl` (pas de service k3s ; `wsl --shutdown` se simule par `docker restart`),
  le script d'installation `get.k3s.io`, le noyau WSL, le forwarding `localhost` vers
  Windows, le nom de nœud réel. Ces points sont décrits « tels que sur WSL » et
  signalés.
- Toute commande écrite dans un `04-*.md` doit avoir été **exécutée** dans le bac à
  sable correspondant (ou sur un vrai WSL), et les sorties citées doivent être les
  sorties réelles (tailles, statuts, messages d'erreur, colonnes de `kubectl get`).

## 8. Checklist avant de considérer un labo terminé

- [ ] Les 4 `.md` existent **dans les trois langues** (`fr/`, `nl/`, `en/`) et
      respectent le plan de la section 4.
- [ ] Les 12 `.pdf` sont générés et chaque `01-*.pdf` fait ≤ 5 pages (dans les trois
      langues).
- [ ] Chaque question du `02` a sa réponse détaillée dans le `03`, même numérotation.
- [ ] La théorie contient au moins un encadré `Podman` (partie Docker) ou `k3s` +
      `Rappel Docker` (partie Kubernetes), et des encadrés « domaine » pour chaque
      notion extérieure au sujet.
- [ ] Toutes les commandes du `04` ont été **exécutées réellement** (bac à sable ou WSL)
      et fonctionnent avec Podman ≥ 4.9 rootless (partie Docker) ou k3s v1.34 (partie
      Kubernetes).
- [ ] Les fichiers de `files/` sont présents et cohérents avec le texte du labo ; les
      manifestes YAML passent `kubectl apply --dry-run=client -f`.
- [ ] Section « Nettoyage » présente à la fin du labo pratique, avec `rm -f -t 0`
      (Docker) ou `kubectl delete namespace labNN` (Kubernetes).
- [ ] `python3 tools/lint_lang.py labs/NN-*` ne signale aucun calque, et chaque langue a
      été relue **sans la source à côté** (section 2).
- [ ] Le `README.md` liste le labo.
