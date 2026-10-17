# Labo 15 — Questions

---

### Question 1 [Compréhension]

Un collègue monte le répertoire des données PostgreSQL avec un volume `hostPath: /data/pg` « parce que ça marche sur k3s ». Expliquez pourquoi cela « marche », ce qui se passera sur un cluster à trois nœuds après une panne, et ce que la chaîne PVC → PV → StorageClass apporte.

### Question 2 [Diagnostic]

```bash
$ kubectl apply -f pvc.yaml
persistentvolumeclaim/data created
$ kubectl get pvc
NAME   STATUS    VOLUME   CAPACITY   ACCESS MODES   STORAGECLASS   AGE
data   Pending                                      local-path     2m
```

Deux minutes sans volume. Est-ce une erreur ? Quelle propriété de la StorageClass explique cet état, et qu'est-ce qui fera passer la PVC en `Bound` ?

### Question 3 [Prédiction]

Une PVC `demo-data` est liée à un PV de classe `local-path` (politique `Delete`). Décrivez ce qui arrive aux données dans chaque cas : (a) suppression du Pod qui l'utilise ; (b) suppression de la PVC ; (c) suppression du namespace ; (d) `kubectl scale statefulset db --replicas=0` pour une PVC créée par `volumeClaimTemplates`.

### Question 4 [Analyse]

Comparez un Deployment PostgreSQL à `replicas: 1` avec une PVC et un StatefulSet à `replicas: 1` avec `volumeClaimTemplates` : nom du Pod après recréation, nom de la PVC, Service, et ce qui se passe si l'on passe à `replicas: 3` dans chaque cas.

### Question 5 [Compréhension]

Qu'est-ce qu'un Service *headless*, en quoi diffère-t-il du Service `api` du labo 13, et pourquoi un StatefulSet en exige-t-il un ? Donnez le nom DNS complet du premier Pod d'un StatefulSet `db` dans le namespace `lab15`.

### Question 6 [Diagnostic]

```bash
$ kubectl logs db-0
initdb: error: directory "/var/lib/postgresql/data" exists but is not empty
initdb: hint: If you want to create a new database system, either remove or empty the directory "/var/lib/postgresql/data" or run initdb with an argument other than "/var/lib/postgresql/data".
```

Le volume est neuf. Qu'y a-t-il dedans, qui l'a mis là, et quelle variable du StatefulSet évite le problème ?

### Question 7 [Analyse]

Expliquez ce que fait `local-path` quand une PVC est consommée sur un cluster k3s à **deux** nœuds : où est créé le volume, quelle contrainte est ajoutée au PV, et ce qui arrive au Pod si ce nœud tombe. Qu'utiliserait-on à la place sur EKS, et qu'est-ce qui change dans la PVC ?

### Question 8 [Diagnostic]

Un StatefulSet `db` à `replicas: 3` a été déployé « pour avoir de la haute disponibilité ». L'équipe découvre que les données écrites via `db-0` ne sont pas visibles via `db-1`. Expliquez ce qu'ils ont réellement déployé, pourquoi Kubernetes ne peut pas faire mieux seul, et ce qu'il faut utiliser.

### Question 9 [Prédiction]

```bash
kubectl delete statefulset db
kubectl get pvc
kubectl apply -f statefulset-db.yaml
kubectl exec db-0 -- psql -U postgres -c "SELECT count(*) FROM clients;"
```

Que montre `get pvc` après la suppression, et que renvoie le `SELECT` après la recréation ? Pourquoi ce comportement est-il voulu, et quelle commande ferait réellement disparaître les données ?

### Question 10 [Analyse]

Trois modes d'accès : `ReadWriteOnce`, `ReadOnlyMany`, `ReadWriteMany`. Pour chacun, donnez un exemple de volume qui le permet, un usage légitime, et dites pourquoi un disque de cloud (EBS, Azure Disk) ne peut pas faire `ReadWriteMany`. Que se passe-t-il si deux Pods sur deux nœuds réclament la même PVC `ReadWriteOnce` ?

### Question 11 [Analyse]

Une équipe sauvegarde sa base en copiant le répertoire `/var/lib/rancher/k3s/storage/pvc-…` du nœud toutes les nuits, avec `rsync`, pendant que PostgreSQL tourne. Rappelez le problème du labo 06, puis donnez les deux approches correctes dans un cluster et ce qu'un opérateur automatise.

### Question 12 [Compréhension]

Quelles différences de comportement un StatefulSet a-t-il lors d'un rolling update par rapport à un Deployment (ordre, parallélisme, `maxSurge`), et pourquoi ces différences sont-elles nécessaires pour une base de données ?

### Question 13 [Analyse]

Dans quels cas une équipe choisit-elle une base **managée hors du cluster** plutôt qu'un StatefulSet ou un opérateur dedans ? Donnez trois critères de décision, dites ce que l'application voit dans chaque cas (Service, ConfigMap, Secret), et ce qui reste identique dans les manifestes de l'API.
