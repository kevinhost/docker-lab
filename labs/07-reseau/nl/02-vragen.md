# Lab 07 — Vragen

---

### Vraag 1 [Diagnose]

De Spring Boot-API start in haar container met `SPRING_DATASOURCE_URL=jdbc:postgresql://localhost:5432/app` en stopt met `Connection refused`. PostgreSQL draait nochtans in de container `db`, op hetzelfde user-defined netwerk, en `podman exec db pg_isready` antwoordt `accepting connections`. Verklaar, corrigeer, en zeg waar `localhost` naar wijst in elk van de twee containers.

### Vraag 2 [Begrip]

Op een Ubuntu/WSL toont `podman inspect --format '{{.NetworkSettings.IPAddress}}' api` een lege regel, terwijl `podman exec api ip -4 addr` wel degelijk een adres toont — hetzelfde als dat van de WSL-distributie. Wat gebeurt er, en wat zou je moeten veranderen opdat de container een adres `10.88.0.x` krijgt?

### Vraag 3 [Voorspelling]

```bash
podman run -d --name a --network podman alpine sleep 1d
podman run -d --name b --network podman alpine sleep 1d
podman exec b ping -c1 10.88.0.2
podman exec b ping -c1 a
```

Voorspel het resultaat van de twee `ping`-commando's, en daarna wat er verandert als je `--network podman` vervangt door `--network stack` na een `podman network create stack`. Verklaar het verschil aan de hand van een veld uit `podman network inspect`.

### Vraag 4 [Analyse]

De Dockerfile van de API bevat `EXPOSE 8080`. Een collega start `podman run -d --name api api:1.0`, doet daarna `curl localhost:8080/actuator/health` vanuit WSL, en krijgt `Connection refused`. Hij voegt `-p 8080:8080` toe: nu werkt het. Hij besluit dat `EXPOSE` "nergens toe dient". Heeft hij gelijk? Waartoe dient `EXPOSE`, en wie leest het?

### Vraag 5 [Diagnose]

```bash
$ podman run -d --name web -p 80:80 nginx:alpine
Error: rootlessport cannot expose privileged port 80, you can add 'net.ipv4.ip_unprivileged_port_start=80' to /etc/sysctl.conf (currently 1024), or choose a larger port number (>= 1024): listen tcp 0.0.0.0:80: bind: permission denied
```

Waarom komt deze fout niet voor bij Docker (in klassieke modus)? Geef drie manieren om de site op poort 80 van de machine te serveren, en zeg welke je in het bedrijf zou kiezen.

### Vraag 6 [Voorspelling]

`web` (nginx, `proxy_pass http://api:8080/`) en `api` draaien op het netwerk `stack`; `curl localhost:18080/api/actuator/health` geeft `200`. Je voert uit:

```bash
podman rm -f -t 0 api
podman run -d --name andere --network stack alpine sleep 1d
podman run -d --name api --network stack api:1.0
```

Wat geeft dezelfde `curl` nu, en waarom, terwijl `podman run --rm --network stack alpine wget -qO- http://api:8080/actuator/health` perfect werkt? Hoe herstel je het?

### Vraag 7 [Analyse]

In de logs van nginx verschijnt elk verzoek dat van je Windows-browser komt met, als clientadres, het adres van de container `web` zelf (`10.89.0.10`). Verklaar waar dat adres vandaan komt, waarin dat verschilt van Docker als root, en welk gevolg dat heeft voor een applicatie die logt of beperkt op basis van het IP-adres.

### Vraag 8 [Begrip]

Kan een container tot twee netwerken behoren? Beschrijf een concreet gebruiksgeval voor de stack `web`/`api`/`db`, de nodige commando's, en wat `podman inspect api --format '{{json .NetworkSettings.Networks}}'` dan toont.

### Vraag 9 [Diagnose]

Een collega start zijn API met `--network host` "om het eenvoudig te houden". Noem twee dingen die anders of helemaal niet meer werken in vergelijking met een bridge-netwerk, en één geval waarin `--network host` gerechtvaardigd is. En wat gebeurt er, in rootless, als de applicatie op poort 80 luistert?

### Vraag 10 [Analyse]

Vergelijk een **netwerk** `stack` met daarin `web` en `api` met een **pod** `stackpod` met dezelfde twee containers: hoe verwijst nginx in elk geval naar de API, waar declareer je `-p`, en wat toont `podman ps --pod` extra? Waarom gaat dit tweede model jou aan, ook als je nooit `podman pod` gebruikt?

### Vraag 11 [Analyse]

Tijdens de ontwikkeling wil je DBeaver (op Windows) aansluiten op de database `db` van het netwerk `stack`, zonder dat de database bereikbaar is voor andere machines op het bedrijfsnetwerk. Geef de exacte `-p`-optie, zeg waarom de Windows-browser die poort toch bereikt ondanks `127.0.0.1`, en waarom je dit in productie nooit doet.

### Vraag 12 [Diagnose]

```bash
$ podman network rm stack
Error: "stack" has associated containers with it. Use -f to forcibly delete containers and pods: network is being used
```

Wat doet `-f` precies, waarom is dat een slecht idee in een opruimreeks, en wat is de juiste volgorde?

### Vraag 13 [Analyse]

Het frontendteam roept de API rechtstreeks aan vanuit de browser op `http://localhost:8080` (gepubliceerde poort van `api`) en worstelt met CORS-fouten. Het ops-team stelt voor om alleen `web` te publiceren en `/api/` door nginx te laten doorsturen. Leg uit waarom dat het CORS-probleem wegneemt, welke andere voordelen het oplevert, en welke regel van `nginx.conf` het werk doet.
