# Lab 01 — Vragen

*Antwoord zonder de theorie erbij te nemen. Eén tot vijf zinnen volstaan; het gaat om je redenering, niet om de juiste vaktermen.*

---

### Vraag 1 [Begrip]

Een collega beweert: "Een container is een kleine virtuele machine met een minimale Linux erin." Wat klopt er niet aan die uitspraak? Leg ook uit waarom deze verwarring concrete gevolgen heeft voor opstarttijd en schijfgebruik.

### Vraag 2 [Analyse]

De image `postgres:16-alpine` is ongeveer 250 MB groot en bevat een volledige Linux-mappenstructuur (`/bin`, `/etc`, `/usr`…). Toch luidt het dat "er geen OS in een container zit". Beide uitspraken zijn waar. Leg uit wat er werkelijk in die image zit, en wat er van een besturingssysteem in **ontbreekt**.

### Vraag 3 [Analyse]

Je start twee containers van dezelfde image `nginx:alpine`. Op de host toont `ps aux | grep nginx` twee groepen processen. Vanuit de eerste container toont `ps` echter alleen de eigen processen. Welk kernelmechanisme zit hierachter, en waarom is dit **geen** beveiliging in de strikte zin van het woord?

### Vraag 4 [Diagnose]

Een collega die Docker gebruikt, toont je dit:

```
Client: Docker Engine - Community
 Version:  29.7.2
Cannot connect to the Docker daemon at unix:///var/run/docker.sock.
Is the docker daemon running?
```

Leg uit wat er op zijn machine aan de hand is (twee waarschijnlijke oorzaken) en waarom het geen zin heeft om aan zijn commando te sleutelen. Leg ook uit waarom jij deze melding **niet** kunt krijgen met rootless Podman onder WSL.

### Vraag 5 [Begrip]

"Een image draait niet." Onderbouw die uitspraak, en leg vervolgens uit wat de engine concreet aan de image toevoegt op het moment dat je `podman run` uitvoert.

### Vraag 6 [Analyse]

Je start een PostgreSQL-container, maakt er een database met tabellen in aan, en verwijdert die container daarna met `podman rm`. Vervolgens start je een nieuwe container van **dezelfde image**. Zijn je gegevens er nog? Onderbouw je antwoord met de structuur image/schrijflaag — en zeg of de image door jouw werk veranderd is.

### Vraag 7 [Analyse]

Je start tien containers van de image `eclipse-temurin:21-jre-alpine` (ongeveer 210 MB). Hoeveel extra schijfruimte kost dat, ruwweg? Leg het mechanisme uit dat dit antwoord mogelijk maakt.

### Vraag 8 [Diagnose]

In een rootless Podman-container toont `id` de waarde `uid=0(root)`. Op de WSL-host toont `podman top <container> user,huser` `root` in de kolom USER en `1000` in de kolom HUSER. Wat betekent die dubbele identiteit, welke namespace veroorzaakt ze, en wat kan die "root" werkelijk uitrichten als hij via een mount in `/etc/shadow` van de host probeert te schrijven?

### Vraag 9 [Begrip]

Je bedrijf verbiedt om op productieservers gebruikers aan de groep `docker` toe te voegen, en eist dat iedereen via `sudo` werkt, met auditspoor. Welke veiligheidsredenering zit achter die regel, en waarom valt die hele discussie weg met rootless Podman?

### Vraag 10 [Analyse]

Zet de volgende commando's om naar hun lange vorm (`podman <object> <actie>`), en zeg voor elk commando op welk **type object** het werkt:

```bash
podman ps -a
podman images
podman rmi nginx:alpine
podman rm web
```

Waarom volgen `podman ps` en `podman images` niet dezelfde naamgevingslogica?

### Vraag 11 [Diagnose]

Vanuit je Ubuntu-terminal onder WSL geeft `podman run --rm alpine uname -r` als resultaat `6.6.87.2-microsoft-standard-WSL2`. Een collega krijgt op een native Ubuntu-server `6.8.0-45-generic` met exact hetzelfde commando. Leg uit waar elk van beide waarden vandaan komt, en wat dit betekent voor de bewering "containers zijn licht" op een Windows-machine.

### Vraag 12 [Analyse]

Een slecht geschreven applicatie in een container belandt in een oneindige lus en slokt al het beschikbare RAM op. Voorkomt de `pid`-namespace dat ze de andere containers schaadt? Welk mechanisme moet je hiervoor wél inzetten, en wat gebeurt er als niemand het geconfigureerd heeft?

### Vraag 13 [Begrip]

In het bedrijf wordt de image van de Spring Boot-backend, gebouwd door de CI, gepromoveerd van integratie naar acceptatie en vervolgens naar productie, **zonder dat ze opnieuw gebouwd wordt**. De acceptatieservers draaien onder Docker, productie onder Podman. Welke eigenschappen maken deze werkwijze mogelijk, en welk risico loop je als je de image bij elke stap opnieuw bouwt vanuit dezelfde broncode?

### Vraag 14 [Analyse]

Een ontwikkelaar zet `alias docker=podman` in zijn `.bashrc` en beweert: "alles wat voor Docker geschreven is, zal werken". Geef twee voorbeelden waarin dat zonder meer klopt, en twee situaties waarin de andere architectuur van Podman (geen daemon, rootless) het gedrag merkbaar verandert.
