# Labo 09 — Questions

---

### Question 1 [Compréhension]

Un collègue a un script `demarrer.sh` de trente lignes de `podman network create`, `podman volume create` et `podman run`, et un `arreter.sh` qui fait l'inverse. « Ça marche, pourquoi Compose ? » Donnez trois choses que `podman compose up` / `down` savent et que ses scripts ne savent pas, sans parler de longueur.

### Question 2 [Diagnostic]

Le fichier `.env` à côté de `compose.yaml` contient `APP_MESSAGE=bonjour depuis dotenv`. Après `podman compose up -d`, `curl localhost:18080/api/` renvoie toujours le message par défaut. Pourtant `podman compose config` ne signale aucune erreur. Expliquez ce que `.env` fait réellement, et où `APP_MESSAGE` aurait dû être déclaré.

### Question 3 [Prédiction]

Deux versions de la dépendance de `api` vers `db` :

```yaml
depends_on: [db]
```
```yaml
depends_on:
  db:
    condition: service_healthy
```

Pour une vraie API Spring Boot, décrivez ce qui se passe au `up -d` dans chaque cas (ordre, logs, état final), et pourquoi la seconde forme exige un bloc `healthcheck` sur `db`.

### Question 4 [Diagnostic]

```yaml
api:
  image: localhost/api:1.0
  healthcheck:
    test: ["CMD", "curl", "-f", "http://localhost:8080/actuator/health"]
    interval: 5s
    retries: 3
```

Après trente secondes, `podman compose ps` montre `api` en `(unhealthy)` et `web` n'a jamais démarré, alors que `curl localhost:18080` fonctionnait avant l'ajout du healthcheck. Diagnostiquez avec une commande, corrigez, et dites pourquoi l'image est en cause.

### Question 5 [Analyse]

Comparez, dans `compose.yaml`, `- pgdata:/var/lib/postgresql/data` (avec `volumes: pgdata:` en bas) et `- ./data:/var/lib/postgresql/data` : qui crée le répertoire, à qui appartiennent les fichiers en rootless, que fait `down -v` dans chaque cas, et lequel choisir pour la base de la stack.

### Question 6 [Prédiction]

Un développeur clone le projet dans `~/travail/stack-v2/` au lieu de `~/travail/stack/`, lance `podman compose up -d`, et constate une base **vide** : « Compose a perdu mes données ! » Le fichier n'a pas de clé `name:`. Expliquez, montrez avec `podman volume ls` ce qui s'est passé, et donnez deux façons d'éviter le problème.

### Question 7 [Diagnostic]

```bash
$ podman compose -f compose.yaml -f compose.prod.yaml up -d
$ podman compose exec api env | grep APP_PROFILE
APP_PROFILE=dev
$ podman exec stack_api_1 env | grep APP_PROFILE
APP_PROFILE=prod
```

Deux commandes, deux réponses pour le même conteneur. Laquelle dit la vérité, d'où vient l'autre, et comment éviter la confusion ?

### Question 8 [Analyse]

`compose.prod.yaml` met `restart: unless-stopped` sur les trois services. Sur un serveur Linux avec Docker, que se passe-t-il après un redémarrage de la machine ? Sur votre WSL avec Podman rootless, après `wsl --shutdown` ? Expliquez la différence et ce qu'il faut utiliser à la place avec Podman.

### Question 9 [Compréhension]

`podman compose up -d --scale api=2` crée `stack_api_1` et `stack_api_2`. Comment `web` répartit-il les requêtes entre les deux, sans aucune configuration ? Pourquoi `--scale web=2` échouerait-il ? Et que faut-il faire avant `podman compose down` avec podman-compose ?

### Question 10 [Diagnostic]

```bash
$ podman compose up -d
Error: creating container storage: the container name "stack_db_1" is already in use by 3e5c2093…
```

D'où vient ce conteneur, pourquoi `up` ne le réutilise-t-il pas, et quelle est la séquence de réparation sans perdre le volume ?

### Question 11 [Analyse]

Dans `compose.yaml`, la base reçoit son mot de passe par `secrets: [db_password]` et `POSTGRES_PASSWORD_FILE`, le secret étant déclaré `file: ./db_password.txt`. Comparez avec `environment: POSTGRES_PASSWORD: S3cr3t` : où la valeur apparaît-elle dans chaque cas (`podman compose config`, `podman inspect`, Git) ? Que faut-il faire de `db_password.txt`, et que change `external: true` ?

### Question 12 [Analyse]

Faites correspondre chaque élément de notre `compose.yaml` à son équivalent Kubernetes, en une ligne chacun : un `service` avec `image`, `ports`, le volume `pgdata`, le `healthcheck`, le `depends_on`, le réseau implicite, `env_file`, `secrets`. Lequel n'a **pas** d'équivalent direct, et pourquoi ?

### Question 13 [Analyse]

L'équipe propose de déployer la production avec `podman compose -f compose.yaml -f compose.prod.yaml up -d` sur une seule VM. Dans quels cas est-ce une décision raisonnable ? Citez quatre choses que cette solution ne fournit pas, et le signal qui indique qu'il est temps de passer à un orchestrateur.
