# Lab 15 — Questions

---

### Question 1 [Understanding]

A colleague mounts the PostgreSQL data directory with a `hostPath: /data/pg` volume "because it works on k3s". Explain why it "works", what will happen on a three-node cluster after a failure, and what the PVC → PV → StorageClass chain brings.

### Question 2 [Diagnosis]

```bash
$ kubectl apply -f pvc.yaml
persistentvolumeclaim/data created
$ kubectl get pvc
NAME   STATUS    VOLUME   CAPACITY   ACCESS MODES   STORAGECLASS   AGE
data   Pending                                      local-path     2m
```

Two minutes with no volume. Is it an error? Which StorageClass property explains this state, and what will move the PVC to `Bound`?

### Question 3 [Prediction]

A `demo-data` PVC is bound to a `local-path` PV (policy `Delete`). Describe what happens to the data in each case: (a) deletion of the Pod that uses it; (b) deletion of the PVC; (c) deletion of the namespace; (d) `kubectl scale statefulset db --replicas=0` for a PVC created by `volumeClaimTemplates`.

### Question 4 [Analysis]

Compare a PostgreSQL Deployment at `replicas: 1` with a PVC and a StatefulSet at `replicas: 1` with `volumeClaimTemplates`: the Pod's name after recreation, the PVC's name, the Service, and what happens if you move to `replicas: 3` in each case.

### Question 5 [Understanding]

What is a *headless* Service, how does it differ from the `api` Service of lab 13, and why does a StatefulSet require one? Give the full DNS name of the first Pod of a `db` StatefulSet in the `lab15` namespace.

### Question 6 [Diagnosis]

```bash
$ kubectl logs db-0
initdb: error: directory "/var/lib/postgresql/data" exists but is not empty
initdb: hint: If you want to create a new database system, either remove or empty the directory "/var/lib/postgresql/data" or run initdb with an argument other than "/var/lib/postgresql/data".
```

The volume is new. What is inside it, who put it there, and which StatefulSet variable avoids the problem?

### Question 7 [Analysis]

Explain what `local-path` does when a PVC is consumed on a **two-node** k3s cluster: where the volume is created, which constraint is added to the PV, and what happens to the Pod if that node goes down. What would be used instead on EKS, and what changes in the PVC?

### Question 8 [Diagnosis]

A `db` StatefulSet at `replicas: 3` was deployed "to get high availability". The team discovers that data written through `db-0` is not visible through `db-1`. Explain what they actually deployed, why Kubernetes alone cannot do better, and what must be used.

### Question 9 [Prediction]

```bash
kubectl delete statefulset db
kubectl get pvc
kubectl apply -f statefulset-db.yaml
kubectl exec db-0 -- psql -U postgres -c "SELECT count(*) FROM clients;"
```

What does `get pvc` show after the deletion, and what does the `SELECT` return after recreation? Why is this behaviour intended, and which command would actually make the data disappear?

### Question 10 [Analysis]

Three access modes: `ReadWriteOnce`, `ReadOnlyMany`, `ReadWriteMany`. For each, give an example of a volume that allows it, a legitimate use, and say why a cloud disk (EBS, Azure Disk) cannot do `ReadWriteMany`. What happens if two Pods on two nodes claim the same `ReadWriteOnce` PVC?

### Question 11 [Analysis]

A team backs up its database by copying the node's `/var/lib/rancher/k3s/storage/pvc-…` directory every night with `rsync`, while PostgreSQL is running. Recall the lab 06 problem, then give the two correct approaches in a cluster and what an operator automates.

### Question 12 [Understanding]

How does a StatefulSet behave differently from a Deployment during a rolling update (order, parallelism, `maxSurge`), and why are those differences necessary for a database?

### Question 13 [Analysis]

In which cases does a team choose a **managed database outside the cluster** rather than a StatefulSet or an operator inside it? Give three decision criteria, say what the application sees in each case (Service, ConfigMap, Secret), and what stays identical in the API's manifests.
