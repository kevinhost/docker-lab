# Labo 06 — Questions

---

### Question 1 [Compréhension]

Un collègue affirme : « J'ai fait `podman stop db` puis `podman start db`, mes tables sont toujours là. Les données d'un conteneur persistent donc très bien, pas besoin de volume. » Qu'a-t-il observé de vrai ? Dans quelles situations courantes ses données disparaîtront-elles quand même ?

### Question 2 [Diagnostic]

Vous lancez :

```bash
podman run -d --name web -p 18080:80 -v html:/usr/share/nginx/html:ro nginx:alpine
```

Votre dossier `html/` contient `index.html` avec « Version 1 », mais `curl localhost:18080` renvoie la page d'accueil par défaut de nginx. Expliquez précisément ce qui s'est passé, d'où vient cette page par défaut, et corrigez la commande.

### Question 3 [Diagnostic]

```bash
$ ls ~/.local/share/containers/storage/volumes/pgdata/_data
ls: cannot open directory '…/pgdata/_data': Permission denied
```

« Pourtant je suis root dans le conteneur, et c'est mon répertoire personnel ! » Expliquez pourquoi ce refus est normal, à qui appartiennent ces fichiers vus de l'hôte, et donnez la commande qui permet de les lister.

### Question 4 [Prédiction]

```bash
podman run -d --name db -e POSTGRES_PASSWORD=alpha -v pgdata:/var/lib/postgresql/data postgres:16-alpine
podman rm -f -t 0 db
podman run -d --name db -e POSTGRES_PASSWORD=bravo -v pgdata:/var/lib/postgresql/data postgres:16-alpine
```

Quel mot de passe permet de se connecter au second conteneur : `alpha`, `bravo`, les deux ? Pourquoi ?

### Question 5 [Analyse]

Pour chacun des besoins suivants, choisissez entre volume nommé, bind mount et tmpfs, et justifiez en une phrase : (a) les sources d'un front Angular pendant le développement ; (b) les fichiers de PostgreSQL ; (c) le `nginx.conf` d'un reverse proxy ; (d) les fichiers intermédiaires d'une conversion PDF qui peuvent atteindre 2 Go.

### Question 6 [Diagnostic]

```bash
$ mkdir sortie
$ podman run --rm --user 1000 -v ./sortie:/out alpine sh -c 'id -u; echo x > /out/f'
1000
sh: can't create /out/f: Permission denied
$ ls -ln sortie
total 0        ← le dossier appartient à 1000:1000
```

L'utilisateur 1000 ne peut pas écrire dans un dossier qui appartient à l'UID 1000. Expliquez le paradoxe et proposez deux corrections différentes.

### Question 7 [Prédiction]

Vous relancez la commande de la question 6 avec `-v ./sortie:/out:U`. Elle réussit. Que montre maintenant `ls -ln sortie` sur l'hôte, pour le propriétaire du dossier et du fichier ? Comment rendre le dossier à votre utilisateur ?

### Question 8 [Analyse]

Sur un serveur de test, `podman volume ls` affiche quatorze volumes dont le nom est un hash de 64 caractères. D'où viennent-ils ? Comment savoir, pour chacun, s'il est encore utilisé et par quoi ? Comment éviter que la liste s'allonge ? Et pourquoi `podman volume prune` n'est-il pas la bonne réponse réflexe ?

### Question 9 [Compréhension]

Un collègue sauvegarde la base de production avec `tar czf backup.tgz` sur le répertoire du volume, toutes les nuits, pendant que PostgreSQL tourne. Les sauvegardes sont là, personne n'a jamais testé une restauration. Quel est le risque exact ? Quelles sont les deux manières correctes de faire, et laquelle choisir pour une sauvegarde quotidienne ?

### Question 10 [Analyse]

Comparez `podman volume export pgdata -o pgdata.tar` et

```bash
podman run --rm -v pgdata:/data:ro -v ./:/backup alpine tar czf /backup/pgdata.tgz -C /data .
```

Qu'est-ce que la seconde commande fait exactement, et pourquoi a-t-elle besoin d'un conteneur pour archiver un répertoire qui est sur votre disque ? Laquelle fonctionne aussi avec Docker ?

### Question 11 [Analyse]

Pourquoi recommande-t-on de déposer un secret déchiffré (clé privée, jeton) dans un tmpfs plutôt que dans la couche writable du conteneur, alors que les deux disparaissent à la suppression du conteneur ? Quelle contrepartie le tmpfs a-t-il sur la mémoire ?

### Question 12 [Diagnostic]

La commande `podman run --rm -v ./conf:/etc/app:ro alpine cat /etc/app/app.yaml` fonctionne sur votre WSL. Sur un serveur RHEL 9 de l'entreprise, le même fichier, les mêmes droits, elle échoue : `cat: can't open '/etc/app/app.yaml': Permission denied`. Même avec `--user 0`. Diagnostiquez, corrigez, et expliquez pourquoi la correction est inoffensive sur Ubuntu.

### Question 13 [Analyse]

L'équipe veut faire tourner **deux** conteneurs de l'API Spring Boot derrière un répartiteur de charge, et prévoit de stocker les documents envoyés par les utilisateurs dans un volume nommé `uploads` monté sur `/app/uploads`. Qu'est-ce qui va mal se passer ? Quelle solution adopte-t-on en entreprise, et quel rapport avec le principe « un conteneur est jetable » ?
