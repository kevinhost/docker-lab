# Labo 03 — Questions

---

### Question 1 [Compréhension]

`docker run alpine` rend la main immédiatement, `docker run nginx` bloque le terminal, et
`docker run -it alpine sh` ouvre un shell. Expliquez ces trois comportements avec **une
seule et même règle**.

### Question 2 [Diagnostic]

Un développeur conteneurise l'API maison et écrit dans son image un script de démarrage :

```sh
#!/bin/sh
java -jar /app/api.jar &
echo "API demarree"
```

Le conteneur affiche bien « API demarree » puis s'arrête aussitôt avec le code `0`.
Expliquez précisément ce qui se passe, et corrigez le script.

### Question 3 [Analyse]

Vous lancez `docker run -d --name veille alpine sleep 300`, puis `docker stop veille`. La
commande met **10 secondes** à revenir et le conteneur termine avec le code `137`. Or
`sleep` n'a rien à sauvegarder. Pourquoi ne s'est-il pas arrêté immédiatement, et pourquoi
`137` plutôt que `143` ?

### Question 4 [Analyse]

Reprenez la question 3, mais avec `docker run -d --init --name veille alpine sleep 300`.
Le `docker stop` revient cette fois **instantanément** et le code de sortie est `143`.
Qu'est-ce que `--init` a changé, exactement ?

### Question 5 [Compréhension]

Différenciez `-i` et `-t`. Que se passe-t-il concrètement si vous lancez
`docker run -t alpine sh` (sans `-i`) puis tapez `ls` ? Et `docker run -i alpine sh` (sans
`-t`) ?

### Question 6 [Diagnostic]

Un collègue lance `docker attach mon-api` pour consulter les logs, appuie sur `Ctrl+C` pour
sortir… et la production tombe. Expliquez ce qui s'est passé, et donnez les deux façons
correctes d'atteindre son but initial.

### Question 7 [Analyse]

Après un incident, `docker ps -a` affiche :

```
NAMES     STATUS
api       Exited (137) 4 minutes ago
worker    Exited (143) 4 minutes ago
batch     Exited (127) 4 minutes ago
```

Pour chacun des trois, dites ce qui s'est très probablement produit et quelle commande vous
lanceriez ensuite pour confirmer.

### Question 8 [Analyse]

Votre application Spring Boot écrit ses logs dans `/var/log/api/application.log` grâce à
`logging.file.name`, comme sur les anciens serveurs. `docker logs api` ne renvoie rien.
Expliquez pourquoi, et dites pourquoi la « solution » consistant à monter ce dossier sur
l'hôte reste une mauvaise réponse.

### Question 9 [Compréhension]

`docker stop` puis `docker start` sur un conteneur PostgreSQL : les données sont-elles
conservées ? Et après `docker rm` puis un nouveau `docker run` ? Expliquez la différence
avec le mécanisme sous-jacent.

### Question 10 [Analyse]

Comparez `--restart=always` et `--restart=unless-stopped` : décrivez un scénario précis où
les deux se comportent différemment, et dites lequel choisir pour un service de production
sur une machine unique.

### Question 11 [Diagnostic]

Un conteneur avec `--restart=on-failure:5` a redémarré cinq fois puis s'est définitivement
arrêté. Où trouvez-vous les logs de la **première** tentative, celle qui contient la cause
initiale ? Que se passe-t-il si vous faites `docker restart` avant d'avoir regardé ?

### Question 12 [Analyse]

Un conteneur consomme 100 % d'un cœur et ne répond plus. Vous voulez savoir ce qu'il fait
avant de le tuer. Classez ces commandes de la moins à la plus intrusive, et dites ce que
chacune vous apprend : `docker logs`, `docker top`, `docker stats`, `docker exec`,
`docker inspect`.

### Question 13 [Compréhension]

Pourquoi ne met-on pas l'API Spring Boot et sa base PostgreSQL dans le même conteneur, alors
que ce serait plus simple à démarrer ? Donnez trois conséquences concrètes, en vous
appuyant sur ce que vous savez du cycle de vie.

### Question 14 [Analyse]

`docker run --rm` est recommandé pour les commandes ponctuelles, mais **déconseillé** pour
un service en production. Expliquez le raisonnement dans les deux cas — que perd-on
exactement quand un conteneur de production disparaît à sa sortie ?
