# Lab 11 — Vragen

---

### Vraag 1 [Begrip]

Een collega beweert: "Met `restart: always` en twee Compose-VM's achter een load balancer heb ik hetzelfde als Kubernetes." Noem drie concrete situaties waarin die architectuur faalt en een cluster het wel redt, en benoem voor elk het onderdeel van het control plane dat ingrijpt.

### Vraag 2 [Voorspelling]

```bash
kubectl apply -f pod-api.yaml
kubectl apply -f pod-api.yaml
kubectl create -f pod-api.yaml
```

Voorspel de uitvoer van elk van de drie commando's, en leg dan aan de hand van dit voorbeeld uit wat "declaratief" en "idempotent" betekenen.

### Vraag 3 [Voorspelling]

```bash
kubectl run web --image=docker.io/library/nginx:alpine
kubectl create deployment api --image=localhost/api:1.0
kubectl delete pod web
kubectl delete pod $(kubectl get pods -l app=api -o jsonpath='{.items[0].metadata.name}')
kubectl get pods
```

Wat toont de laatste `get pods`, en waarom hebben de twee verwijderingen een verschillend effect? Welk object, dat in het eerste geval ontbreekt, maakt het verschil?

### Vraag 4 [Diagnose]

```bash
$ podman images | grep api
localhost/api   1.0   dd522f8992fd   2 days ago   209 MB
$ kubectl apply -f pod-api.yaml && sleep 10 && kubectl get pods
NAME   READY   STATUS             RESTARTS   AGE
api    0/1     ImagePullBackOff   0          10s
```

De image bestaat nochtans. Leg uit wat de kubelet geprobeerd heeft, waarom hij de image niet vindt, en geef het commando dat het probleem oplost en het veld van het manifest dat ertoe doet.

### Vraag 5 [Diagnose]

`kubectl get pods` antwoordt `No resources found in default namespace.` terwijl `kubectl get pods -A` je Pod `api` wel degelijk toont. Verklaar, geef twee manieren om de Pod te zien, en het commando dat vermijdt dat je telkens `-n` moet typen.

### Vraag 6 [Analyse]

Voor de keten `web → api` zijn er twee ontwerpen: (a) één Pod met twee containers `web` en `api`; (b) twee Pods, één per dienst. Hoe verwijst nginx naar de API in elk geval? Welk lijkt op lab 07, welk op lab 09? En welk kies je in productie, en waarom?

### Vraag 7 [Analyse]

Open `/etc/rancher/k3s/k3s.yaml`: wat bevat het, in drie elementen? Waarom is `--write-kubeconfig-mode 644` aanvaardbaar op je werkstation en geweigerd op een gedeelde server? En wat gebeurt er als je dat bestand ongewijzigd naar een andere machine kopieert om je cluster aan te sturen?

### Vraag 8 [Diagnose]

```bash
$ kubectl get pods
The connection to the server localhost:8080 was refused - did you specify the right host or port?
```

Nochtans zegt `sudo systemctl status k3s` `active (running)`. Wat zoekt `kubectl`, waarom mikt het op `localhost:8080`, en wat zijn de twee mogelijke correcties?

### Vraag 9 [Begrip]

Als de API server tien minuten stilvalt, wat gebeurt er dan met de Pods die op de nodes draaien? Wat kun je niet meer doen? En wat doet de kubelet met een Pod die tijdens die panne sterft? Leid daaruit af waarom men zegt dat de API server "de enige deur" is, en niet "de motor".

### Vraag 10 [Analyse]

Dit zijn de Events van een `kubectl describe pod web`:

```
Normal  Scheduled  default-scheduler  Successfully assigned lab11/web to wsl-ubuntu
Normal  Pulling    kubelet            Pulling image "docker.io/library/nginx:alpine"
Normal  Pulled     kubelet            Successfully pulled image … in 3.75s
Normal  Created    kubelet            Created container: web
Normal  Started    kubelet            Started container web
```

Wijs elke regel toe aan een onderdeel en zeg wat het gedaan heeft; zet er dan de stappen van een `podman run` uit lab 03 tegenover. Wat doet het cluster méér, en wie doet hier niets omdat er maar één node is?

### Vraag 11 [Diagnose]

Een Pod staat al vijf minuten in `Pending`, zonder enig IP in `kubectl get pods -o wide`. Wat zijn de twee meest waarschijnlijke oorzaken, welk commando onderscheidt ze, en hoe ziet de boodschap er in elk geval uit?

### Vraag 12 [Analyse]

Een ontwikkelaar die alleen k3s kent, komt bij een team op EKS terecht. Noem vier dingen die op k3s "vanzelf" werken en die hij op een beheerd cluster zal moeten leren aanvragen of instellen, en twee dingen die helemaal niet veranderen.

### Vraag 13 [Analyse]

De YAML die `podman generate kube` in het praktijklab produceert, bevat een volume `hostPath` naar `~/labo-docker/07/nginx-pod.conf` en een `hostPort: 18090`. Leg uit waarom die twee velden aanvaardbaar zijn op jouw machine en onaanvaardbaar in een clustermanifest, en door welke Kubernetes-objecten je ze vervangt.
