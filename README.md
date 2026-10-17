# Docker Lab — série de labos Docker puis Kubernetes en ligne de commande

Un labo 0 de fondamentaux Linux, puis dix-sept labos d'auto-formation pour comprendre
Docker **puis Kubernetes**, tels qu'ils sont utilisés en entreprise sur une stack
Spring Boot + Angular + PostgreSQL — en pratiquant dans **Ubuntu sous WSL 2** (Windows) :

- **Partie 1 — Docker (00-10)** avec **Podman rootless**, dont la CLI est identique à
  celle de Docker ;
- **Partie 2 — Kubernetes (11-17)** avec **k3s**, un Kubernetes certifié mono-nœud, qui
  redéploie la même stack sur un vrai cluster (Deployment, Service, Ingress, ConfigMap,
  Secret, StatefulSet, Helm).

Chaque labo existe en **trois langues** : français (`fr/`), néerlandais (`nl/`) et anglais
(`en/`), et se compose de quatre PDF :

| # | Rôle | Contenu |
|---|------|---------|
| 01 | Théorie | Le cours, 5 pages max, avec des encadrés « domaine » (Linux, Java, Réseau, Windows/WSL, Sécurité…) et des encadrés « Podman » ou « k3s » |
| 02 | Questions | 14 questions de raisonnement, de diagnostic et de prédiction |
| 03 | Réponses | Corrigé détaillé : réponse, mécanisme, nuance, exemple vérifiable |
| 04 | Labo pratique | Manipulation guidée au terminal, sorties réelles, nettoyage nommé |

## Labos

### Partie 1 — Docker (pratiqué avec Podman)

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

### Partie 2 — Kubernetes (pratiqué avec k3s)

Commence une fois la partie Docker terminée. Prérequis : la même Ubuntu/WSL avec
`systemd` activé, `sudo`, au moins 4 Go de RAM pour WSL ; k3s s'installe à l'étape 0 du
labo 11 (`curl -sfL https://get.k3s.io | sudo sh -s - --write-kubeconfig-mode 644`) et
fournit `kubectl`, Traefik (Ingress), ServiceLB et la StorageClass `local-path`.

| # | Dossier | Concept | État |
|---|---------|---------|------|
| 11 | `11-pourquoi-kubernetes` | Du Compose au cluster : architecture, modèle déclaratif, `kubectl`, premier Pod, passerelle `podman kube play` | à écrire |
| 12 | `12-pods-deployments-et-probes` | Pod, labels, ReplicaSet, Deployment, rolling update, probes, images Podman dans k3s | à écrire |
| 13 | `13-services-et-ingress` | ClusterIP / NodePort / LoadBalancer, CoreDNS, Ingress Traefik, chaîne web → api | à écrire |
| 14 | `14-configmaps-et-secrets` | ConfigMap, Secret, env vs fichiers montés, profils Spring | à écrire |
| 15 | `15-stockage-et-statefulsets` | PV / PVC / StorageClass, StatefulSet Postgres, headless Service | à écrire |
| 16 | `16-ressources-et-exploitation` | Namespaces, requests/limits, QoS, `kubectl top`, diagnostic, RBAC de base | à écrire |
| 17 | `17-helm-et-livraison` | Helm, Kustomize, tags et digests, CI/CD vers le cluster, GitOps, k3s vs clusters managés | à écrire |

## Mode d'emploi

1. Lisez `01-*.pdf` (théorie) dans votre langue.
2. Répondez aux questions de `02-*.pdf` **sans relire** la théorie, par écrit.
3. Comparez avec `03-*.pdf`.
4. Faites le labo pratique `04-*.pdf` au terminal, dans Ubuntu sous WSL 2 avec Podman
   (l'installation est décrite à l'étape 0 du labo 01) puis k3s (étape 0 du labo 11).

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
`python3 tools/lint_lang.py` repère les calques et faux amis (anglais → FR/NL,
FR → NL/EN) dans la prose des trois langues.

## Vérifier les commandes sans Podman ni k3s installés

`tools/podman-sandbox.sh up` crée un Podman 5.x rootless (cgroups délégués) dans un
conteneur Docker privilégié, pour exécuter réellement chaque commande des labos :

```bash
tools/podman-sandbox.sh up
tools/podman-sandbox.sh copy-labs
tools/podman-sandbox.sh run 'podman run --rm alpine uname -r'
tools/podman-sandbox.sh shell
```

Pour la partie Kubernetes, `tools/k3s-sandbox.sh` (créé avec le labo 11) lance de la
même façon l'image `rancher/k3s:v1.34.1-k3s1` en conteneur privilégié, avec `kubectl`,
et importe les images construites dans le bac à sable Podman.

---

*Dutch (Belgium) — Elk labo bestaat ook in het Nederlands (`nl/`). English — every lab
is also available in English (`en/`). The terminal commands are identical in all three
versions.*
