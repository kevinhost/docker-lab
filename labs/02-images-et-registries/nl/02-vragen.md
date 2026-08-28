# Lab 02 — Vragen

*Antwoord zonder de theorie te herlezen. Verantwoord altijd: een bewering zonder mechanisme is niets waard.*

---

### Vraag 1 [Begrip]

Schrijf de **volledige en expliciete** naam die de engine bouwt uit elk van deze schrijfwijzen, leg de regel uit waarmee men weet of het eerste deel een registry of een namespace is — en zeg voor elke naam hoe Podman zich gedraagt tegenover de korte naam:

```
nginx
bitnami/nginx
registry.mijnbedrijf.be:5000/basis/nginx:1.25
```

### Vraag 2 [Analyse]

Twee servers, A en B, hebben op dezelfde dag `mijnapp/api:2.3` gepulld. Drie weken later rolt het team alleen op B opnieuw uit, met hetzelfde commando `podman pull mijnapp/api:2.3`. Er verschijnt een bug op B en niet op A. Hoe is dat mogelijk, terwijl de versie "dezelfde" is? Welk commando bewijst het, en welke praktijk had het probleem vermeden?

### Vraag 3 [Diagnose]

Een ontwikkelaar merkt dat `podman images` 40 images oplijst voor een totaal van 62 GB in de kolom `SIZE`, terwijl zijn WSL-schijf maar 100 GB is en hij nooit een plaatsprobleem had. Heeft hij echt 62 GB aan images? Leg uit, geef het commando dat het echte cijfer toont, en zeg waar die bestanden fysiek staan op zijn werkpost.

### Vraag 4 [Analyse]

Een Dockerfile bevat:

```dockerfile
COPY credentials.json /tmp/credentials.json
RUN ./configure.sh && rm /tmp/credentials.json
```

De auteur beweert dat het geheim niet in de uiteindelijke image zit, aangezien hij het verwijderd heeft. Heeft hij gelijk? Leg precies uit wat de image bevat, en waarom de `rm` niets aan het probleem verandert.

### Vraag 5 [Begrip]

Je pusht een tweede versie van je Spring Boot-image naar de registry. Ze weegt 310 MB, de vorige woog 308 MB. De `push` draagt nochtans maar 61 MB over. Leg het mechanisme uit, en zeg dan wat je in je Dockerfile zou moeten veranderen als de push telkens de volle 310 MB overdroeg.

### Vraag 6 [Diagnose]

```bash
$ podman images
REPOSITORY          TAG       IMAGE ID       SIZE
localhost/api       2.0       f3a1b9c02d11   310 MB
localhost/api       1.9       f3a1b9c02d11   310 MB
<none>              <none>    8b2c74e91a03   295 MB
```

Becommentarieer deze uitvoer: hoeveel verschillende images zie je werkelijk? Waar komt de regel `<none>` vandaan? Wat gebeurt er precies als je `podman rmi api:1.9` typt? En waarom `localhost/`?

### Vraag 7 [Analyse]

Je collega bouwt de backend-image op zijn MacBook M3 en pusht ze naar de registry. De uitrol op de acceptatieserver faalt met `exec /usr/bin/java: exec format error`. Stel de diagnose, en geef twee manieren om het op te lossen — één om meteen te deblokkeren, de andere opdat het probleem zich niet meer voordoet.

### Vraag 8 [Begrip]

`podman save` en `podman export` leveren allebei een `.tar`-archief. In welke situatie is elk de juiste keuze? Wat verlies je precies als je `export` gebruikt om een Spring Boot-image naar een geïsoleerde site te vervoeren? En wat verandert `--format oci-archive` aan een `save`?

### Vraag 9 [Analyse]

Na een `podman pull` van een image van 400 MB voer je hetzelfde commando opnieuw uit: het eindigt in enkele seconden, zonder download. Wat heeft de engine werkelijk gecontroleerd — en waarom kostte dat bijna niets op het netwerk?

### Vraag 10 [Diagnose]

De CI van je bedrijf faalt met tussenpozen op `podman pull node:22-alpine`, met de melding `toomanyrequests: You have reached your pull rate limit`. Er is niets aan de pipeline veranderd. Leg de oorzaak uit, waarom ze "met tussenpozen" opduikt, en de twee klassieke antwoorden in een bedrijf.

### Vraag 11 [Diagnose]

Je start een lokale registry (`podman run -d -p 5000:5000 registry:2`), en dan:

```
$ podman push localhost:5000/basis/demo:1.0
Error: … pinging container registry localhost:5000: Get "https://localhost:5000/v2/":
http: server gave HTTP response to HTTPS client
```

Je collega, onder Docker, heeft die melding nooit gezien met dezelfde registry. Leg het verschil in filosofie uit, geef twee manieren om de `push` te laten slagen — en zeg waarom een van beide nooit in een geversioneerd configuratiebestand mag belanden.

### Vraag 12 [Diagnose]

Een `podman rmi mijn-api:1.0` geeft:

```
Error: image used by 4c2e9a1b7d33…: image is in use by a container: consider listing
external containers and force-removing image
```

Leg de situatie uit, zeg waarom de engine weigert, geef de **nette** manier om het op te lossen — en zeg dan wat `podman rmi -f` doet en waarom dat hier een slecht idee is.

### Vraag 13 [Analyse]

`podman history` op een image toont meerdere lagen van `0B` en één laag van `180MB`. Wat zijn de lagen van `0B`, en waarom bestaan ze dan toch? Hoe helpt die lezing je concreet om een image kleiner te maken?

### Vraag 14 [Begrip]

Je team twijfelt tussen drie tagstrategieën voor de backend-image: (a) `api:latest`, overschreven bij elke build, (b) `api:1.4.2`, volgens de applicatieversie, (c) `api:1.4.2-b318-a9f3c21`, met buildnummer en Git-*commit*. Bespreek de drie vanuit het oogpunt van **rollback in productie** en **incidentdiagnose**.
