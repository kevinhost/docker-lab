# Lab 13 — Vragen

---

### Vraag 1 [Diagnose]

```bash
$ kubectl get pods
NAME                   READY   STATUS             RESTARTS     AGE
api-6c7bb54fc5-2vs4k   1/1     Running            0            27s
web-5588bd85f8-j5nl5   0/1     CrashLoopBackOff   2 (6s ago)   27s
$ kubectl logs deploy/web --tail=1
nginx: [emerg] host not found in upstream "api" in /etc/nginx/conf.d/default.conf:15
```

De API draait. Waarom vindt nginx `api` niet, terwijl dezelfde configuratie in lab 07 werkte met een gewoon Podman-netwerk? Wat moet je aanmaken, en waarom herstart `web` daarna vanzelf?

### Vraag 2 [Begrip]

Leg uit wat, voor een Service `api`, het **cluster-IP**, de **DNS-naam** en de **EndpointSlices** zijn, wie elk ervan bijhoudt, en waarom `ping 10.43.3.7` nooit antwoordt terwijl `wget http://10.43.3.7:8080/` werkt.

### Vraag 3 [Voorspelling]

Een Service `api` selecteert `app: api`; het Deployment gaat van 2 naar 3 replica's, dan verwijder je met de hand een Pod, dan breek je de readiness van een Pod. Wat toont `kubectl get endpointslices` na elke handeling, en wat heeft een client die ondertussen `api:8080` aanriep, gezien?

### Vraag 4 [Diagnose]

`kubectl get svc api` toont een ClusterIP en de poort `8080/TCP`, maar `kubectl get endpointslices -l kubernetes.io/service-name=api` geeft een slice **zonder adres**, en Traefik antwoordt `503`. De Pods zijn `1/1 Running`. Noem de twee mogelijke oorzaken, het commando dat ze onderscheidt, en de correctie voor elk.

### Vraag 5 [Analyse]

Vergelijk `ClusterIP`, `NodePort` en `LoadBalancer` om de frontend op je WSL bloot te stellen: welke URL in elk geval, wat k3s meer doet dan kale Kubernetes voor het derde, en waarom een tweede `LoadBalancer`-Service op poort 80 bij k3s `<pending>` zou blijven.

### Vraag 6 [Begrip]

Vanuit een Pod in de namespace `lab13` werkt `wget http://api:8080/`; vanuit een Pod in de namespace `default` faalt het. Verklaar aan de hand van de inhoud van `/etc/resolv.conf` van een Pod, en geef de naam die je vanuit `default` moet gebruiken.

### Vraag 7 [Analyse]

Een Service verdeelt verbindingen, geen verzoeken. Leg het verschil uit, wat dat oplevert voor een HTTP/1.1-client met *keep-alive* (of een JDBC-verbinding) tegenover drie replica's, en wat de Ingress aan dat gedrag verandert.

### Vraag 8 [Diagnose]

```yaml
spec:
  selector:
    app: api
  ports:
    - port: 80
      targetPort: 8080
```

Met dit Service faalt `wget http://api:8080/` (`Connection refused`) maar werkt `wget http://api/`. Verklaar de twee poorten, en zeg wat nginx in zijn `proxy_pass` moet schrijven.

### Vraag 9 [Analyse]

Beschrijf het pad van een verzoek `GET /api/actuator/health` dat een Windows-browser naar `http://localhost/` stuurt in onze k3s-stack: elk doorlopen onderdeel, in volgorde, en de twee betrokken reverse proxies. Hoe vereenvoudig je de keten door één regel te verplaatsen?

### Vraag 10 [Begrip]

Wat is het verschil tussen een `Ingress`-object en een *Ingress controller*? Wat gebeurt er als je een Ingress toepast in een cluster zonder controller? En waarom wijst een `503 Service Unavailable` van Traefik bijna altijd op een probleem met endpoints en niet met Traefik?

### Vraag 11 [Diagnose]

Een team rolt zijn applicatie uit op EKS met de manifesten die op k3s geschreven zijn. Het `LoadBalancer`-Service krijgt wel een publiek IP, maar de Ingress blijft zonder `ADDRESS` en de site antwoordt niet. Wat ontbreekt, en waarom "werkte" het op k3s?

### Vraag 12 [Analyse]

De frontend roept de API aan via `/api/` (zelfde origin) in plaats van via `http://api.example.com` (andere origin). Herinner eraan waarom (lab 07), en zeg dan waar die `/api/`-routering in onze stack kan gebeuren — nginx of Ingress — en wat de voordelen zijn om ze aan de Ingress toe te vertrouwen.

### Vraag 13 [Analyse]

Een ontwikkelaar wil vanuit DBeaver op Windows de PostgreSQL-database van het cluster bereiken. Drie opties: `kubectl port-forward svc/db 5432:5432`, een NodePort, een LoadBalancer. Rangschik ze naar toenemende blootstelling, zeg welke in productie aanvaardbaar is en waarom, en welk object nog ontbreekt opdat `db` een naam heeft (hint: lab 15).
