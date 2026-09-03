# Docker Lab — série de labos Docker/Podman en ligne de commande

Un labo 0 de fondamentaux Linux puis dix labos d'auto-formation pour comprendre Docker **tel qu'il est utilisé en entreprise**
sur une stack Spring Boot + Angular + PostgreSQL — en pratiquant avec **Podman sur WSL 2**
(Windows), dont la CLI est identique à celle de Docker.

Chaque labo existe en **trois langues** : français (`fr/`), néerlandais (`nl/`) et anglais
(`en/`), et se compose de quatre PDF :

| # | Rôle | Contenu |
|---|------|---------|
| 01 | Théorie | Le cours, 5 pages max, avec des encadrés « domaine » (Linux, Java, Réseau, Windows/WSL, Sécurité…) et des encadrés « Podman » |
| 02 | Questions | 14 questions de raisonnement, de diagnostic et de prédiction |
| 03 | Réponses | Corrigé détaillé : réponse, mécanisme, nuance, exemple vérifiable |
| 04 | Labo pratique | Manipulation guidée au terminal, sorties réelles, nettoyage nommé |

## Labos

| # | Dossier | Concept | État |
|---|---------|---------|------|
| 00 | [`labs/00-fondamentaux-linux`](labs/00-fondamentaux-linux) | Fondamentaux Linux : noyau, processus, signaux, permissions, shell, ports | FR · NL · EN |
| 01 | [`labs/01-conteneurs-et-architecture`](labs/01-conteneurs-et-architecture) | Qu'est-ce qu'un conteneur ; Docker vs Podman ; WSL 2 ; rootless | FR · NL · EN |
| 02 | [`labs/02-images-et-registries`](labs/02-images-et-registries) | Images, tags, digests, couches, registries, noms complets | FR · NL · EN |
| 03 | [`labs/03-cycle-de-vie-conteneurs`](labs/03-cycle-de-vie-conteneurs) | `run/stop/kill/rm`, PID 1, signaux, codes de sortie, conmon, restart | FR · NL · EN |
| 04 | [`labs/04-dockerfile`](labs/04-dockerfile) | Dockerfile, contexte, cache, `CMD`/`ENTRYPOINT`, `ARG`/`ENV`, Buildah | FR · NL · EN |
| 05 | [`labs/05-multistage-et-optimisation`](labs/05-multistage-et-optimisation) | Multi-stage, images de base, distroless, cache mounts | FR · NL · EN |
| 06 | `06-donnees-et-volumes` | Volumes, bind mounts, UID en rootless | à écrire |
| 07 | `07-reseau` | Réseaux, DNS interne, `-p`, pasta | à écrire |
| 08 | `08-configuration-et-secrets` | Variables, profils Spring, secrets | à écrire |
| 09 | `09-docker-compose` | `podman compose` / Compose | à écrire |
| 10 | `10-exploitation-et-bonnes-pratiques` | Exploitation, Quadlet, limites, `prune`, sécurité | à écrire |

## Mode d'emploi

1. Lisez `01-*.pdf` (théorie) dans votre langue.
2. Répondez aux questions de `02-*.pdf` **sans relire** la théorie, par écrit.
3. Comparez avec `03-*.pdf`.
4. Faites le labo pratique `04-*.pdf` au terminal, dans Ubuntu sous WSL 2 avec Podman
   (l'installation est décrite à l'étape 0 du labo 01).

Le labo 00 est le seul à ne demander **ni Podman ni installation** : une distribution
Ubuntu 24.04 sous WSL 2 suffit. Si les processus, les signaux, `chmod`, le `PATH` et
les redirections vous sont déjà familiers, vous pouvez le survoler — mais faites ses
questions pour vérifier.

## Régénérer les PDF

```bash
./build.sh                          # tout
./build.sh labs/04-dockerfile       # un labo, trois langues
./build.sh labs/04-dockerfile/nl    # une langue
```

La source de vérité est le Markdown ; les PDF sont régénérés (Chrome headless).

## Vérifier les commandes sans Podman installé

`tools/podman-sandbox.sh up` crée un Podman 5.x rootless (cgroups délégués) dans un
conteneur Docker privilégié, pour exécuter réellement chaque commande des labos :

```bash
tools/podman-sandbox.sh up
tools/podman-sandbox.sh copy-labs
tools/podman-sandbox.sh run 'podman run --rm alpine uname -r'
tools/podman-sandbox.sh shell
```

---

*Dutch (Belgium) — Elk labo bestaat ook in het Nederlands (`nl/`). English — every lab
is also available in English (`en/`). The terminal commands are identical in all three
versions.*
