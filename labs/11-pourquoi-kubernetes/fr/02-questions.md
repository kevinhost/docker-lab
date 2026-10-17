# Labo 11 — Questions

---

### Question 1 [Compréhension]

Un collègue affirme : « Avec `restart: always` et deux VM Compose derrière un équilibreur, j'ai la même chose que Kubernetes. » Citez trois situations concrètes où cette architecture échoue et où un cluster s'en sort, et nommez pour chacune le composant du control plane qui agit.

### Question 2 [Prédiction]

```bash
kubectl apply -f pod-api.yaml
kubectl apply -f pod-api.yaml
kubectl create -f pod-api.yaml
```

Prédisez la sortie de chacune des trois commandes, puis expliquez ce que « déclaratif » et « idempotent » veulent dire à travers cet exemple.

### Question 3 [Prédiction]

```bash
kubectl run web --image=docker.io/library/nginx:alpine
kubectl create deployment api --image=localhost/api:1.0
kubectl delete pod web
kubectl delete pod $(kubectl get pods -l app=api -o jsonpath='{.items[0].metadata.name}')
kubectl get pods
```

Que montre le dernier `get pods`, et pourquoi les deux suppressions ont-elles des effets différents ? Quel objet, absent dans le premier cas, fait la différence ?

### Question 4 [Diagnostic]

```bash
$ podman images | grep api
localhost/api   1.0   dd522f8992fd   2 days ago   209 MB
$ kubectl apply -f pod-api.yaml && sleep 10 && kubectl get pods
NAME   READY   STATUS             RESTARTS   AGE
api    0/1     ImagePullBackOff   0          10s
```

L'image existe pourtant. Expliquez ce que le kubelet a tenté, pourquoi il ne trouve pas l'image, et donnez la commande qui règle le problème ainsi que le champ du manifeste qui compte.

### Question 5 [Diagnostic]

`kubectl get pods` répond `No resources found in default namespace.` alors que `kubectl get pods -A` liste bien votre Pod `api`. Expliquez, donnez deux façons de voir le Pod, et la commande qui évite de répéter `-n` à chaque fois.

### Question 6 [Analyse]

Pour la chaîne `web → api`, deux conceptions : (a) un seul Pod avec deux conteneurs `web` et `api` ; (b) deux Pods, un par service. Comment nginx désigne-t-il l'API dans chaque cas ? Lequel ressemble au labo 07, lequel au labo 09 ? Et lequel choisit-on en production, pourquoi ?

### Question 7 [Analyse]

Ouvrez `/etc/rancher/k3s/k3s.yaml` : que contient-il, en trois éléments ? Pourquoi `--write-kubeconfig-mode 644` est-il acceptable sur votre poste et refusé sur un serveur partagé ? Et que se passe-t-il si vous copiez ce fichier tel quel sur une autre machine pour piloter votre cluster ?

### Question 8 [Diagnostic]

```bash
$ kubectl get pods
The connection to the server localhost:8080 was refused - did you specify the right host or port?
```

Pourtant `sudo systemctl status k3s` dit `active (running)`. Que cherche `kubectl`, pourquoi vise-t-il `localhost:8080`, et quelles sont les deux corrections possibles ?

### Question 9 [Compréhension]

Si l'API server s'arrête pendant dix minutes, que deviennent les Pods qui tournent sur les nœuds ? Que ne pouvez-vous plus faire ? Et que fait le kubelet d'un Pod qui meurt pendant cette panne ? Déduisez-en pourquoi l'on dit que l'API server est « la seule porte », pas « le moteur ».

### Question 10 [Analyse]

Voici les Events d'un `kubectl describe pod web` :

```
Normal  Scheduled  default-scheduler  Successfully assigned lab11/web to wsl-ubuntu
Normal  Pulling    kubelet            Pulling image "docker.io/library/nginx:alpine"
Normal  Pulled     kubelet            Successfully pulled image … in 3.75s
Normal  Created    kubelet            Created container: web
Normal  Started    kubelet            Started container web
```

Attribuez chaque ligne à un composant et dites ce qu'il a fait ; puis mettez en regard les étapes d'un `podman run` du labo 03. Qu'est-ce que le cluster fait en plus, et qui ne fait rien ici parce qu'il n'y a qu'un nœud ?

### Question 11 [Diagnostic]

Un Pod reste en `Pending` depuis cinq minutes, sans aucune IP dans `kubectl get pods -o wide`. Quelles sont les deux causes les plus probables, quelle commande les départage, et à quoi ressemble le message dans les deux cas ?

### Question 12 [Analyse]

Un développeur qui n'a connu que k3s rejoint une équipe sur EKS. Citez quatre choses qui marchent « toutes seules » sur k3s et qu'il devra apprendre à demander ou à configurer sur un cluster managé, et deux choses qui ne changent strictement pas.

### Question 13 [Analyse]

Le YAML produit par `podman generate kube` au labo pratique contient un volume `hostPath` vers `~/labo-docker/07/nginx-pod.conf` et un `hostPort: 18090`. Expliquez pourquoi ces deux champs sont acceptables sur votre machine et inacceptables dans un manifeste de cluster, et par quels objets Kubernetes on les remplace.
