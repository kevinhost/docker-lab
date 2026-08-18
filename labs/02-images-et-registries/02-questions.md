# Labo 02 — Questions

*Répondez sans relire la théorie. Justifiez toujours : une affirmation sans mécanisme ne
vaut rien.*

---

### Question 1 [Compréhension]

Écrivez le nom **complet et explicite** que Docker construit à partir de chacune de ces
trois écritures, et expliquez la règle qui permet à Docker de savoir si la première partie
du nom est un registry ou un namespace :

```
nginx
bitnami/nginx
registry.masociete.fr:5000/socle/nginx:1.25
```

### Question 2 [Analyse]

Deux serveurs, A et B, ont tiré `monapp/api:2.3` le même jour. Trois semaines plus tard,
l'équipe redéploie sur B uniquement, avec la même commande `docker pull monapp/api:2.3`.
Un bug apparaît sur B et pas sur A. Comment cela est-il possible alors que la version est
« la même » ? Quelle commande permet de le prouver, et quelle pratique aurait évité le
problème ?

### Question 3 [Diagnostic]

Un développeur observe que `docker images` liste 40 images pour un total de 62 Go dans la
colonne `SIZE`, alors que son disque ne fait que 100 Go et qu'il n'a jamais eu de problème
de place. A-t-il vraiment 62 Go d'images ? Expliquez, et donnez la commande qui affiche le
chiffre réel.

### Question 4 [Analyse]

Un Dockerfile contient :

```dockerfile
COPY credentials.json /tmp/credentials.json
RUN ./configure.sh && rm /tmp/credentials.json
```

L'auteur affirme que le secret n'est pas dans l'image finale puisqu'il l'a supprimé.
A-t-il raison ? Expliquez précisément ce que contient l'image, et pourquoi le `rm` ne
change rien au problème.

### Question 5 [Compréhension]

Vous poussez une deuxième version de votre image Spring Boot vers le registry. Elle pèse
310 Mo, la précédente pesait 308 Mo. Le `push` ne transfère pourtant que 61 Mo. Expliquez
le mécanisme, puis dites ce que vous devriez changer dans votre Dockerfile si le push
transférait à chaque fois les 310 Mo.

### Question 6 [Diagnostic]

```bash
$ docker images
REPOSITORY   TAG       IMAGE ID       SIZE
api          2.0       f3a1b9c02d11   310MB
api          1.9       f3a1b9c02d11   310MB
<none>       <none>    8b2c74e91a03   295MB
```

Commentez cette sortie : combien d'images distinctes voyez-vous réellement ? D'où vient la
ligne `<none>` ? Que se passe-t-il exactement si vous tapez `docker rmi api:1.9` ?

### Question 7 [Analyse]

Votre collègue construit l'image du back sur son MacBook M3 et la pousse au registry. Le
déploiement sur le serveur de recette échoue avec `exec /usr/bin/java: exec format error`.
Diagnostiquez, et donnez deux façons de corriger — l'une pour dépanner tout de suite,
l'autre pour que le problème ne se reproduise plus.

### Question 8 [Compréhension]

`docker save` et `docker export` produisent tous deux une archive `.tar`. Dans quelle
situation chacun est-il le bon choix ? Que perd-on précisément si l'on utilise `export`
pour transporter une image Spring Boot vers un site isolé ?

### Question 9 [Analyse]

Après un `docker pull` d'une image de 400 Mo, vous relancez la même commande : elle se
termine en moins d'une seconde avec `Status: Image is up to date`. Que Docker a-t-il
réellement vérifié — et pourquoi cela n'a-t-il presque rien coûté en réseau ?

### Question 10 [Diagnostic]

La CI de votre entreprise échoue par intermittence sur `docker pull node:22-alpine`, avec
le message `toomanyrequests: You have reached your pull rate limit`. Aucun changement n'a
été fait dans le pipeline. Expliquez la cause, pourquoi elle apparaît « par
intermittence », et les deux réponses classiques en entreprise.

### Question 11 [Analyse]

Vous devez expliquer à un nouvel arrivant pourquoi l'entreprise interdit d'utiliser
directement `docker.io/library/postgres:latest` en production, alors que c'est une image
officielle, gratuite et maintenue. Donnez trois arguments distincts, de nature différente.

### Question 12 [Diagnostic]

Un `docker rmi mon-api:1.0` renvoie :

```
Error response from daemon: conflict: unable to delete f3a1b9c02d11 (must be forced)
- image is being used by stopped container 4c2e9a1b7d33
```

Expliquez la situation, dites pourquoi Docker refuse, et donnez la manière **propre** de
résoudre — puis dites ce que fait `docker rmi -f` et pourquoi c'est une mauvaise idée ici.

### Question 13 [Analyse]

`docker history` sur une image montre plusieurs couches de taille `0B` et une couche de
`180MB`. Que sont les couches à `0B`, et pourquoi existent-elles quand même ? En quoi
cette lecture vous aide-t-elle concrètement à réduire la taille d'une image ?

### Question 14 [Compréhension]

Votre équipe hésite entre trois stratégies de tags pour l'image du back :
(a) `api:latest` réécrit à chaque build, (b) `api:1.4.2` suivant la version applicative,
(c) `api:1.4.2-b318-a9f3c21` incluant numéro de build et *commit* Git. Discutez les trois
du point de vue du **retour arrière en production** et du **diagnostic d'incident**.
