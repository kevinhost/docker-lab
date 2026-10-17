# Lab 12 — Vragen

---

### Vraag 1 [Begrip]

Een Deployment `api` met drie replica's is aangemaakt en daarna twee keer bijgewerkt. Hoeveel ReplicaSets bestaan er, hoeveel Pods, en wat toont `kubectl get rs`? Waarom worden de oude ReplicaSets niet verwijderd, en welke instelling begrenst hun aantal?

### Vraag 2 [Diagnose]

```yaml
spec:
  replicas: 2
  selector:
    matchLabels:
      app: api
  template:
    metadata:
      labels:
        app: backend
```

`kubectl apply` weigert dit Deployment. Geef de foutmelding in grote lijnen, leg de geschonden regel uit, en zeg wat er zou gebeuren als het cluster ze aanvaardde.

### Vraag 3 [Voorspelling]

Een Deployment met drie replica's en de standaardstrategie gaat van `api:1.0` naar `api:1.1`. Beschrijf de reeks Events `ScalingReplicaSet` (hoeveel Pods van elke versie bij elke stap), en leg uit waarom het cluster niet meteen drie nieuwe Pods aanmaakt.

### Vraag 4 [Diagnose]

```bash
$ kubectl set image deployment/api api=localhost/api:bad
$ kubectl get pods
NAME                   READY   STATUS    RESTARTS      AGE
api-6c7bb54fc5-c2lhj   1/1     Running   0             32s
api-6c7bb54fc5-km2h6   1/1     Running   0             40s
api-6c7bb54fc5-s9c8f   1/1     Running   0             40s
api-6c87f96dd5-4v6s6   0/1     Error     2 (24s ago)   25s
```

Waarom is er maar één Pod van de nieuwe versie, waarom draaien de drie oude nog, en wat antwoordt `kubectl rollout status`? Geef de twee commando's die de oorzaak onthullen en daarna herstellen.

### Vraag 5 [Analyse]

Een collega stelt een `livenessProbe` in die `/actuator/health` bevraagt, dat `DOWN` teruggeeft zodra de database onbereikbaar is. De database valt vijf minuten uit. Beschrijf wat er met de API gebeurt, waarom dat erger is dan zonder sonde, en wat er had moeten gebeuren.

### Vraag 6 [Voorspelling]

In een Deployment met drie gezonde replica's wijzig je het template zodat de `readinessProbe` poort `8081` bevraagt (waar niets luistert). Wat tonen `kubectl get pods` en `kubectl get deployment api` dertig seconden later? Antwoordt de dienst nog? Dezelfde vraag als je de `livenessProbe` gebroken had.

### Vraag 7 [Begrip]

Leg uit wat `CrashLoopBackOff` is: is het een toestand van de applicatie, van de container of van de kubelet? Waarom liggen de herstarts steeds verder uit elkaar? Welk commando toont de oorzaak, en waarom kan `kubectl logs` zonder optie niets nuttigs tonen?

### Vraag 8 [Analyse]

Vergelijk de `HEALTHCHECK` van lab 10 met een `readinessProbe httpGet`: wie voert de controle uit, waar moet de tool (`wget`, `curl`) staan, welk effect heeft een mislukking, en welke van de twee werkt met een distroless-image?

### Vraag 9 [Diagnose]

`kubectl rollout history deployment/api` toont de revisies `2, 4, 6, 7`: de nummers `1, 3, 5` ontbreken. Leg uit waar die gaten vandaan komen (hint: elke `rollout undo` maakt een revisie aan) en waarom dat geen teken van een probleem is.

### Vraag 10 [Analyse]

Een Deployment heeft `maxSurge: 0` en `maxUnavailable: 1`; een ander heeft `maxSurge: 1` en `maxUnavailable: 0`. Beschrijf voor drie replica's de update in elk geval (aantal Pods op het hoogte- en op het dieptepunt), en zeg welk past bij een cluster met volle nodes en welk bij een dienst die nooit capaciteit mag verliezen.

### Vraag 11 [Diagnose]

Na `kubectl scale deployment api --replicas=5` blijven twee Pods eindeloos in `Pending`, de drie andere zijn `Running`. Wat is de meest waarschijnlijke oorzaak op een k3s met één node, waar lees je ze, en wat gebeurt er als je in die toestand een `rollout` toepast?

### Vraag 12 [Analyse]

Een ontwikkelaar omzeilt Kubernetes: hij doet `kubectl exec` in een Pod, wijzigt een configuratiebestand en herstart het proces met de hand. Beschrijf wat er gebeurt bij de volgende rollout, bij de volgende herstart van de Pod, en op de twee andere replica's. Wat had hij moeten doen (twee objecten uit de volgende labs)?

### Vraag 13 [Analyse]

Een losse `Pod` in een manifest (`kind: Pod`) wordt in productie toegepast "omdat we maar één instantie hebben". Geef vier dingen die deze keuze onmogelijk maakt, vergeleken met een Deployment met `replicas: 1`, en het enige geval waarin een kale Pod het juiste object is.
