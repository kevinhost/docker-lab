# Lab 05 — Vragen

---

### Vraag 1 [Analyse]

Een team levert zijn Spring Boot-API in een image van 950 MB, gebouwd vanuit `maven:3.9-eclipse-temurin-21`. De veiligheidsverantwoordelijke weigert de productie-uitrol. Geef **drie** argumenten die niets met schijfruimte te maken hebben, en zeg dan welk het moeilijkst te verhelpen is anders dan met een multi-stage.

### Vraag 2 [Begrip]

In een multi-stage Dockerfile met drie `FROM`s: welke levert de uiteindelijke image? Wat wordt er van de andere? En als geen enkele `COPY --from` naar de tweede stage verwijst, wat doet Buildah dan — en hoe zie je dat in de uitvoer van `podman build`?

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

De uiteindelijke image is 420 MB in plaats van de verwachte 210 MB, en de broncode zit er nog altijd in. Leg de fout uit en corrigeer ze in één regel.

### Vraag 4 [Analyse]

Je collega wil "tijd winnen" door `ng serve` te containeriseren: de image bevat Node, de projectbronnen, en start de Angular-ontwikkelserver op poort 4200. Het werkt in acceptatie. Geef vier redenen om deze image in productie te weigeren, en beschrijf dan in twee zinnen wat er in de plaats moet gebeuren.

### Vraag 5 [Analyse]

Een team migreert zijn image van `eclipse-temurin:21-jre` (Ubuntu) naar `eclipse-temurin:21-jre-alpine` en wint 120 MB. Twee weken later faalt een PDF-generatietaak in productie met een `UnsatisfiedLinkError`. Leg het waarschijnlijke verband uit, zeg welk commando in elke image het verschil zou hebben getoond, en hoe die migratie had moeten verlopen.

### Vraag 6 [Begrip]

Waarom zegt men dat multi-stage de enige **betrouwbare** bescherming tegen buildgeheimen is, terwijl men het bestand ook met een `rm` kan verwijderen? In welk geval beschermt multi-stage **niet**?

### Vraag 7 [Analyse]

Vergelijk deze twee strategieën voor een Spring Boot-JAR van 50 MB, vanuit het oogpunt van de **uitroltijd** van een fix van één regel: (a) `COPY target/api.jar app.jar`, (b) de extractie in lagen (`-Djarmode=tools … extract --layers`). Becijfer bij benadering wat er in elk geval wordt overgedragen, en zeg waarom (a) in veel bedrijven aanvaardbaar blijft.

### Vraag 8 [Diagnose]

Een CI-build gaat van 90 seconden naar 7 minuten na de overstap naar een nieuwe agent, zonder dat er een bestand veranderd is. De Dockerfile is correct geordend (afhankelijkheden vóór code). Leg uit, en geef twee mechanismen om de 90 seconden terug te winnen — met vermelding, voor een agent die bouwt met rootless Podman, van waar de cache leeft.

### Vraag 9 [Analyse]

Een *distroless* image verkleint het aanvalsoppervlak sterk. Noem twee exploitatiemogelijkheden die je concreet verliest, en zeg hoe een team elk daarvan gewoonlijk compenseert.

### Vraag 10 [Begrip]

`RUN --mount=type=cache,target=/root/.m2 mvn package`: waar worden die gegevens opgeslagen, en waarom verschijnen ze niet in de uiteindelijke image? Wat is het verschil met een `VOLUME`? En wat gebeurt er als men de regel `# syntax=docker/dockerfile:1` vergeet — onder Docker, en dan onder Podman?

### Vraag 11 [Analyse]

Een ontwikkelaar beweert: "Multi-stage dient tot niets voor Angular, aangezien het resultaat toch alleen statische bestanden zijn." Antwoord hem door te beschrijven wat de image zonder multi-stage zou bevatten, en het grootteverschil dat op het spel staat.

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

Vind de fout, en zeg dan welk `podman build`-commando je zou toelaten de echte inhoud van de stage `build` te inspecteren om de diagnose te stellen zonder te gokken.

### Vraag 13 [Analyse]

Je bedrijf legt op dat unittests de bouw van de image doen mislukken. Waar zet je `RUN mvn test` in een multi-stage Dockerfile, en wat is het nadeel van die aanpak tegenover tests die vooraf door de CI worden uitgevoerd?

### Vraag 14 [Analyse]

Twee images van dezelfde applicatie: de ene van 250 MB in één enkele laag, de andere van 280 MB in vijf lagen waarvan vier stabiel. Welke wordt het snelst uitgerold bij een update van de applicatiecode? Verantwoord, en zeg in welke situatie het antwoord omkeert.
