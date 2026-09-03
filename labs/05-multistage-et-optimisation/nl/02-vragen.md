# Lab 05 — Vragen

---

### Vraag 1 [Analyse]

Een team levert zijn Spring Boot-API als een image van 950 MB, gebouwd vanuit `maven:3.9-eclipse-temurin-21`. De veiligheidsverantwoordelijke houdt de productie-uitrol tegen. Geef **drie** argumenten die niets met schijfruimte te maken hebben, en zeg dan welk argument je zonder multi-stage het moeilijkst wegwerkt.

### Vraag 2 [Begrip]

Een multi-stage Dockerfile telt drie `FROM`s. Welke levert de uiteindelijke image, en wat gebeurt er met de andere? En als geen enkele `COPY --from` naar de tweede stage verwijst: wat doet Buildah dan, en hoe zie je dat in de uitvoer van `podman build`?

### Vraag 3 [Diagnose]

Een ontwikkelaar schrijft:

```dockerfile
FROM docker.io/library/maven:3.9-eclipse-temurin-21 AS build
COPY . /app
WORKDIR /app
RUN mvn package -DskipTests

FROM docker.io/library/eclipse-temurin:21-jre-alpine
COPY --from=build /app /app
ENTRYPOINT ["java","-jar","/app/target/api.jar"]
```

De uiteindelijke image weegt 420 MB in plaats van de verwachte 210 MB, en de broncode zit er nog altijd in. Leg de fout uit en corrigeer ze in één regel.

### Vraag 4 [Analyse]

Om "tijd te winnen" containeriseert je collega `ng serve`: de image bevat Node en de projectbronnen, en start de Angular-ontwikkelserver op poort 4200. In acceptatie werkt dat prima. Geef vier redenen om deze image voor productie te weigeren, en beschrijf dan in twee zinnen wat er in de plaats moet komen.

### Vraag 5 [Analyse]

Een team stapt met zijn image over van `eclipse-temurin:21-jre` (Ubuntu) naar `eclipse-temurin:21-jre-alpine` en wint 120 MB. Twee weken later faalt een PDF-generatietaak in productie met een `UnsatisfiedLinkError`. Leg de vermoedelijke oorzaak uit, noem het commando dat in elke image het verschil zou hebben getoond, en beschrijf hoe die migratie had moeten verlopen.

### Vraag 6 [Begrip]

Waarom heet multi-stage de enige **betrouwbare** bescherming tegen buildgeheimen, terwijl je het bestand toch ook met `rm` kunt verwijderen? In welk geval beschermt multi-stage **niet**?

### Vraag 7 [Analyse]

Vergelijk deze twee strategieën voor een Spring Boot-JAR van 50 MB, gemeten aan de **uitroltijd** van een fix van één regel: (a) `COPY target/api.jar app.jar`, (b) extractie in lagen (`-Djarmode=tools … extract --layers`). Maak een ruwe schatting van wat er in elk geval over het netwerk gaat, en leg uit waarom (a) voor veel bedrijven toch volstaat.

### Vraag 8 [Diagnose]

Een CI-build springt van 90 seconden naar 7 minuten na de overstap naar een nieuwe agent, terwijl er geen enkel bestand veranderd is. De Dockerfile is correct geordend (afhankelijkheden vóór code). Leg uit waarom, en geef twee mechanismen om de 90 seconden terug te winnen — vermeld daarbij waar de cache leeft op een agent die met rootless Podman bouwt.

### Vraag 9 [Analyse]

Een *distroless* image verkleint het aanvalsoppervlak sterk. Noem twee mogelijkheden voor de exploitatie die je concreet verliest, en zeg hoe een team elk daarvan gewoonlijk opvangt.

### Vraag 10 [Begrip]

`RUN --mount=type=cache,target=/root/.m2 mvn package`: waar worden die gegevens opgeslagen, en waarom duiken ze nooit op in de uiteindelijke image? Wat is het verschil met een `VOLUME`? En wat gebeurt er als je de regel `# syntax=docker/dockerfile:1` weglaat — eerst onder Docker, dan onder Podman?

### Vraag 11 [Analyse]

Een ontwikkelaar beweert: "Multi-stage heeft geen zin voor Angular — het resultaat is toch maar een hoop statische bestanden." Antwoord hem door te beschrijven wat de image zonder multi-stage zou bevatten, en hoeveel grootte er op het spel staat.

### Vraag 12 [Diagnose]

De volgende Dockerfile faalt met `COPY failed: … /app/dist: no such file or directory`:

```dockerfile
FROM docker.io/library/node:22-alpine AS build
WORKDIR /src
COPY . .
RUN npm ci && npm run build

FROM docker.io/library/nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
```

Vind de fout, en noem dan het `podman build`-commando waarmee je de echte inhoud van de stage `build` kunt bekijken in plaats van te gokken.

### Vraag 13 [Analyse]

Je bedrijf eist dat falende unittests de imagebuild doen mislukken. Waar zet je `RUN mvn test` in een multi-stage Dockerfile, en wat is het nadeel tegenover tests die de CI vooraf uitvoert?

### Vraag 14 [Analyse]

Twee images van dezelfde applicatie: de ene is 250 MB in één enkele laag, de andere 280 MB in vijf lagen, waarvan vier stabiel. Welke rolt het snelst uit wanneer de applicatiecode wijzigt? Verantwoord je antwoord, en zeg in welke situatie het omslaat.
