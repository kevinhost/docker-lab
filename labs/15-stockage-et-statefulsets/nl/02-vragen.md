# Lab 15 — Vragen

---

### Vraag 1 [Begrip]

Een collega mount de gegevensmap van PostgreSQL met een volume `hostPath: /data/pg` "omdat het werkt op k3s". Leg uit waarom het "werkt", wat er op een cluster met drie nodes na een panne zal gebeuren, en wat de keten PVC → PV → StorageClass bijbrengt.

### Vraag 2 [Diagnose]

```bash
$ kubectl apply -f pvc.yaml
persistentvolumeclaim/data created
$ kubectl get pvc
NAME   STATUS    VOLUME   CAPACITY   ACCESS MODES   STORAGECLASS   AGE
data   Pending                                      local-path     2m
```

Twee minuten zonder volume. Is dat een fout? Welke eigenschap van de StorageClass verklaart die toestand, en wat zal de PVC naar `Bound` brengen?

### Vraag 3 [Voorspelling]

Een PVC `demo-data` is gekoppeld aan een PV van klasse `local-path` (beleid `Delete`). Beschrijf wat er met de gegevens gebeurt in elk geval: (a) verwijdering van de Pod die ze gebruikt; (b) verwijdering van de PVC; (c) verwijdering van de namespace; (d) `kubectl scale statefulset db --replicas=0` voor een PVC aangemaakt door `volumeClaimTemplates`.

### Vraag 4 [Analyse]

Vergelijk een PostgreSQL-Deployment met `replicas: 1` en een PVC met een StatefulSet met `replicas: 1` en `volumeClaimTemplates`: naam van de Pod na nieuwe aanmaak, naam van de PVC, Service, en wat er gebeurt als je in elk geval naar `replicas: 3` gaat.

### Vraag 5 [Begrip]

Wat is een *headless* Service, waarin verschilt het van het Service `api` van lab 13, en waarom vereist een StatefulSet er een? Geef de volledige DNS-naam van de eerste Pod van een StatefulSet `db` in de namespace `lab15`.

### Vraag 6 [Diagnose]

```bash
$ kubectl logs db-0
initdb: error: directory "/var/lib/postgresql/data" exists but is not empty
initdb: hint: If you want to create a new database system, either remove or empty the directory "/var/lib/postgresql/data" or run initdb with an argument other than "/var/lib/postgresql/data".
```

Het volume is nieuw. Wat zit erin, wie heeft het erin gezet, en welke variabele van de StatefulSet vermijdt het probleem?

### Vraag 7 [Analyse]

Leg uit wat `local-path` doet wanneer een PVC gebruikt wordt op een k3s-cluster met **twee** nodes: waar wordt het volume aangemaakt, welke beperking wordt aan de PV toegevoegd, en wat gebeurt er met de Pod als die node uitvalt. Wat zou je op EKS in de plaats gebruiken, en wat verandert er in de PVC?

### Vraag 8 [Diagnose]

Een StatefulSet `db` met `replicas: 3` is uitgerold "om hoge beschikbaarheid te hebben". Het team ontdekt dat gegevens geschreven via `db-0` niet zichtbaar zijn via `db-1`. Leg uit wat ze werkelijk uitgerold hebben, waarom Kubernetes alleen niet beter kan, en wat ze moeten gebruiken.

### Vraag 9 [Voorspelling]

```bash
kubectl delete statefulset db
kubectl get pvc
kubectl apply -f statefulset-db.yaml
kubectl exec db-0 -- psql -U postgres -c "SELECT count(*) FROM clients;"
```

Wat toont `get pvc` na de verwijdering, en wat geeft de `SELECT` na de nieuwe aanmaak? Waarom is dat gedrag gewild, en welk commando zou de gegevens werkelijk laten verdwijnen?

### Vraag 10 [Analyse]

Drie toegangsmodi: `ReadWriteOnce`, `ReadOnlyMany`, `ReadWriteMany`. Geef voor elk een voorbeeld van een volume dat het toelaat, een legitiem gebruik, en zeg waarom een cloudschijf (EBS, Azure Disk) geen `ReadWriteMany` kan. Wat gebeurt er als twee Pods op twee nodes dezelfde `ReadWriteOnce`-PVC opeisen?

### Vraag 11 [Analyse]

Een team back-upt zijn database door elke nacht de map `/var/lib/rancher/k3s/storage/pvc-…` van de node te kopiëren met `rsync`, terwijl PostgreSQL draait. Herinner aan het probleem van lab 06, en geef dan de twee correcte benaderingen in een cluster en wat een operator automatiseert.

### Vraag 12 [Begrip]

Welke verschillen in gedrag heeft een StatefulSet bij een rolling update ten opzichte van een Deployment (volgorde, parallellisme, `maxSurge`), en waarom zijn die verschillen nodig voor een database?

### Vraag 13 [Analyse]

In welke gevallen kiest een team een **beheerde database buiten het cluster** in plaats van een StatefulSet of een operator erin? Geef drie beslissingscriteria, zeg wat de applicatie in elk geval ziet (Service, ConfigMap, Secret), en wat identiek blijft in de manifesten van de API.
