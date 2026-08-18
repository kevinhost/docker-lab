# Labo 01 — Questions

*Répondez sans relire la théorie. Une réponse d'une à cinq phrases suffit ; ce qui compte
est le raisonnement, pas le vocabulaire.*

---

### Question 1 [Compréhension]

Un collègue affirme : « Un conteneur, c'est une petite machine virtuelle avec un Linux
minimal dedans. » En une réponse structurée, dites ce qui est faux dans cette phrase, et
expliquez pourquoi cette confusion a des conséquences concrètes sur le temps de démarrage
et l'occupation disque.

### Question 2 [Analyse]

L'image `postgres:16-alpine` pèse environ 250 Mo et contient une arborescence Linux
complète (`/bin`, `/etc`, `/usr`…). Pourtant on dit qu'« il n'y a pas d'OS dans un
conteneur ». Les deux affirmations sont vraies : expliquez ce qui se trouve réellement
dans cette image et ce qui, dans un système d'exploitation, en est **absent**.

### Question 3 [Analyse]

Vous lancez deux conteneurs à partir de la même image `nginx:alpine`. Sur l'hôte, un
`ps aux | grep nginx` montre bien deux jeux de processus. Pourtant, depuis l'intérieur du
premier conteneur, un `ps` ne montre que ses propres processus. Quel mécanisme du noyau
est responsable, et pourquoi ce n'est **pas** de la sécurité au sens strict ?

### Question 4 [Diagnostic]

Vous tapez `docker version` et obtenez :

```
Client: Docker Engine - Community
 Version:  29.7.2
 ...
Cannot connect to the Docker daemon at unix:///var/run/docker.sock.
Is the docker daemon running?
```

Le client fonctionne donc parfaitement. Que s'est-il passé exactement, quelles sont les
**deux** causes les plus probables, et pourquoi est-il inutile de modifier votre commande
pour corriger le problème ?

### Question 5 [Compréhension]

« Une image ne tourne pas. » Justifiez cette phrase, puis expliquez ce que Docker ajoute
concrètement à l'image au moment où vous lancez `docker run`.

### Question 6 [Analyse]

Vous démarrez un conteneur PostgreSQL, vous y créez une base et des tables, puis vous
faites `docker rm` sur ce conteneur. Vous relancez un nouveau conteneur à partir de la
**même image**. Vos données sont-elles là ? Justifiez en vous appuyant sur la structure
image / couche d'écriture — et dites si l'image a été modifiée par votre travail.

### Question 7 [Analyse]

Vous lancez dix conteneurs de l'image `eclipse-temurin:21-jre` (environ 280 Mo). Quel
espace disque supplémentaire cela consomme-t-il, approximativement ? Expliquez le
mécanisme qui rend cette réponse possible.

### Question 8 [Diagnostic]

Un développeur monte un dossier de son poste dans un conteneur avec
`-v /home/dev/data:/data`, mais son `DOCKER_HOST` pointe vers un daemon installé sur un
serveur distant. Le conteneur démarre, et `/data` est vide. Expliquez pourquoi, en vous
appuyant sur l'architecture client/daemon.

### Question 9 [Compréhension]

Votre entreprise interdit d'ajouter des utilisateurs au groupe `docker` sur les serveurs
de production, et exige de passer par `sudo` avec une trace d'audit. Quel est le
raisonnement de sécurité derrière cette règle ?

### Question 10 [Analyse]

Traduisez en forme longue (`docker <objet> <action>`) les commandes suivantes, et dites
pour chacune sur quel **type d'objet** elle agit :

```bash
docker ps -a
docker images
docker rmi nginx:alpine
docker rm web
```

Pourquoi `docker ps` et `docker images` ne suivent-ils pas la même logique de nommage ?

### Question 11 [Diagnostic]

Un ingénieur exécute sur son MacBook :
`docker run --rm alpine cat /proc/version`
et obtient une version de noyau Linux, alors qu'il n'y a aucun noyau Linux sur macOS.
Expliquez ce qu'il voit réellement, et quelle conséquence cela a sur l'affirmation « les
conteneurs sont légers ».

### Question 12 [Analyse]

Une application conteneurisée mal codée part en boucle infinie et consomme toute la RAM
disponible. Le namespace `pid` l'empêche-t-il de nuire aux autres conteneurs ? Quel est
le mécanisme correct à mobiliser, et que se passe-t-il si personne ne l'a configuré ?

### Question 13 [Compréhension]

En entreprise, l'image du back Spring Boot construite par la CI est promue de
l'intégration vers la recette puis la production **sans être reconstruite**. Quelle
propriété des images rend cette pratique possible, et quel risque prend-on si l'on
reconstruit l'image à chaque étape à partir du même code source ?

### Question 14 [Analyse]

Sur quelle machine s'exécute chacune de ces opérations — client ou daemon ? Justifiez en
une ligne chacune : (a) la lecture du fichier `Dockerfile` lors d'un build, (b) l'affichage
coloré du tableau de `docker ps`, (c) le téléchargement d'une image depuis Docker Hub,
(d) la résolution du chemin `.` dans `docker build .`.
