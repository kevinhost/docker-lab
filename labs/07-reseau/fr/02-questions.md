# Labo 07 — Questions

---

### Question 1 [Diagnostic]

L'API Spring Boot démarre dans son conteneur avec `SPRING_DATASOURCE_URL=jdbc:postgresql://localhost:5432/app` et s'arrête sur `Connection refused`. PostgreSQL tourne pourtant dans le conteneur `db`, sur le même réseau user-defined, et `podman exec db pg_isready` répond `accepting connections`. Expliquez, corrigez, et dites ce que `localhost` désigne dans chacun des deux conteneurs.

### Question 2 [Compréhension]

Sur une Ubuntu/WSL, `podman inspect --format '{{.NetworkSettings.IPAddress}}' api` affiche une ligne vide, alors que `podman exec api ip -4 addr` montre bien une adresse — la même que celle de la distribution WSL. Que se passe-t-il, et que faudrait-il changer pour que le conteneur reçoive une adresse `10.88.0.x` ?

### Question 3 [Prédiction]

```bash
podman run -d --name a --network podman alpine sleep 1d
podman run -d --name b --network podman alpine sleep 1d
podman exec b ping -c1 10.88.0.2
podman exec b ping -c1 a
```

Prédisez le résultat des deux `ping`, puis ce qui change si l'on remplace `--network podman` par `--network stack` après un `podman network create stack`. Expliquez la différence par un champ de `podman network inspect`.

### Question 4 [Analyse]

Le Dockerfile de l'API contient `EXPOSE 8080`. Un collègue lance `podman run -d --name api api:1.0` puis `curl localhost:8080/actuator/health` depuis WSL, et obtient `Connection refused`. Il ajoute `-p 8080:8080` : ça marche. Il en conclut que `EXPOSE` « ne sert à rien ». A-t-il raison ? À quoi sert `EXPOSE`, et qui le lit ?

### Question 5 [Diagnostic]

```bash
$ podman run -d --name web -p 80:80 nginx:alpine
Error: rootlessport cannot expose privileged port 80, you can add 'net.ipv4.ip_unprivileged_port_start=80' to /etc/sysctl.conf (currently 1024), or choose a larger port number (>= 1024): listen tcp 0.0.0.0:80: bind: permission denied
```

Pourquoi cette erreur n'apparaît-elle pas avec Docker (en mode classique) ? Donnez trois façons de servir le site sur le port 80 de la machine, et dites laquelle vous choisiriez en entreprise.

### Question 6 [Prédiction]

`web` (nginx, `proxy_pass http://api:8080/`) et `api` tournent sur le réseau `stack` ; `curl localhost:18080/api/actuator/health` renvoie `200`. Vous exécutez :

```bash
podman rm -f -t 0 api
podman run -d --name autre --network stack alpine sleep 1d
podman run -d --name api --network stack api:1.0
```

Que renvoie maintenant le même `curl`, et pourquoi, alors que `podman run --rm --network stack alpine wget -qO- http://api:8080/actuator/health` fonctionne parfaitement ? Comment réparer ?

### Question 7 [Analyse]

Dans les logs de nginx, chaque requête venue de votre navigateur Windows apparaît avec, comme adresse client, l'adresse du conteneur `web` lui-même (`10.89.0.10`). Expliquez d'où vient cette adresse, en quoi cela diffère de Docker root, et quelle conséquence cela a pour une application qui journalise ou limite par adresse IP.

### Question 8 [Compréhension]

Un conteneur peut-il appartenir à deux réseaux ? Décrivez un cas d'usage concret pour la stack `web`/`api`/`db`, les commandes nécessaires, et ce que voit alors `podman inspect api --format '{{json .NetworkSettings.Networks}}'`.

### Question 9 [Diagnostic]

Un collègue lance son API avec `--network host` « pour simplifier ». Citez deux choses qui fonctionnent différemment ou plus du tout par rapport à un réseau bridge, et un cas où `--network host` est légitime. Et que se passe-t-il, en rootless, si l'application écoute sur le port 80 ?

### Question 10 [Analyse]

Comparez un **réseau** `stack` contenant `web` et `api` avec un **pod** `stackpod` contenant les mêmes deux conteneurs : comment nginx désigne-t-il l'API dans chaque cas, où se déclare `-p`, et que montre `podman ps --pod` de plus ? Pourquoi ce second modèle vous concerne-t-il même si vous n'utilisez jamais `podman pod` ?

### Question 11 [Analyse]

En développement, vous voulez brancher DBeaver (sur Windows) à la base `db` du réseau `stack`, sans que la base soit joignable par d'autres machines du réseau d'entreprise. Donnez l'option `-p` exacte, dites pourquoi le navigateur Windows atteint quand même ce port malgré `127.0.0.1`, et pourquoi on ne fait jamais cela en production.

### Question 12 [Diagnostic]

```bash
$ podman network rm stack
Error: "stack" has associated containers with it. Use -f to forcibly delete containers and pods: network is being used
```

Que fait `-f` exactement, pourquoi est-ce une mauvaise idée dans une séquence de nettoyage, et quelle est la séquence correcte ?

### Question 13 [Analyse]

L'équipe front appelle l'API directement depuis le navigateur sur `http://localhost:8080` (port publié de `api`), et se bat avec des erreurs CORS. L'équipe ops propose de ne publier que `web` et de faire relayer `/api/` par nginx. Expliquez pourquoi cela supprime le problème CORS, quels autres bénéfices cela apporte, et quelle ligne de `nginx.conf` fait le travail.
