# Lab 01 — Vragen

*Antwoord zonder de theorie te herlezen. Eén tot vijf zinnen volstaan; wat telt is de redenering, niet het vocabularium.*

---

### Vraag 1 [Begrip]

Een collega beweert: "Een container is een kleine virtuele machine met een minimale Linux erin." Zeg wat er fout is aan die zin, en leg uit waarom die verwarring concrete gevolgen heeft voor de opstarttijd en het schijfgebruik.

### Vraag 2 [Analyse]

De image `postgres:16-alpine` weegt ongeveer 250 MB en bevat een volledige Linux-boomstructuur (`/bin`, `/etc`, `/usr`…). Toch zegt men dat "er geen OS in een container zit". Beide uitspraken zijn waar: leg uit wat er werkelijk in die image zit en wat er, van een besturingssysteem, **ontbreekt**.

### Vraag 3 [Analyse]

Je start twee containers van dezelfde image `nginx:alpine`. Op de host toont `ps aux | grep nginx` twee reeksen processen. Toch toont `ps` vanuit de eerste container alleen zijn eigen processen. Welk kernelmechanisme is verantwoordelijk, en waarom is dit **geen** beveiliging in de strikte zin?

### Vraag 4 [Diagnose]

Een collega die Docker gebruikt, toont je dit:

```
Client: Docker Engine - Community
 Version:  29.7.2
Cannot connect to the Docker daemon at unix:///var/run/docker.sock.
Is the docker daemon running?
```

Leg uit wat er bij hem gebeurd is (twee waarschijnlijke oorzaken), waarom het zinloos is zijn commando te wijzigen — en waarom deze melding jou **niet** kan overkomen met je rootless Podman onder WSL.

### Vraag 5 [Begrip]

"Een image draait niet." Verantwoord die zin, en leg dan uit wat de engine concreet aan de image toevoegt op het moment dat je `podman run` typt.

### Vraag 6 [Analyse]

Je start een PostgreSQL-container, maakt er een database en tabellen in aan, en doet dan `podman rm` op die container. Je start een nieuwe container van **dezelfde image**. Zijn je gegevens er nog? Verantwoord aan de hand van de structuur image / schrijflaag — en zeg of de image door je werk gewijzigd is.

### Vraag 7 [Analyse]

Je start tien containers van de image `eclipse-temurin:21-jre-alpine` (ongeveer 210 MB). Hoeveel extra schijfruimte verbruikt dat, bij benadering? Leg het mechanisme uit dat dit antwoord mogelijk maakt.

### Vraag 8 [Diagnose]

In een rootless Podman-container toont `id` `uid=0(root)`. Op de WSL-host toont `podman top <container> user,huser` `root` in de kolom USER en `1000` in de kolom HUSER. Leg uit wat die dubbele identiteit betekent, welke namespace ze voortbrengt, en wat die "root" werkelijk kan doen als hij via een mount probeert te schrijven in `/etc/shadow` van de host.

### Vraag 9 [Begrip]

Je bedrijf verbiedt het toevoegen van gebruikers aan de groep `docker` op productieservers, en eist dat men via `sudo` met een auditspoor werkt. Wat is de veiligheidsredenering achter die regel, en waarom maakt rootless Podman de vraag overbodig?

### Vraag 10 [Analyse]

Vertaal de volgende commando's naar hun lange vorm (`podman <object> <actie>`), en zeg voor elk op welk **type object** het werkt:

```bash
podman ps -a
podman images
podman rmi nginx:alpine
podman rm web
```

Waarom volgen `podman ps` en `podman images` niet dezelfde naamlogica?

### Vraag 11 [Diagnose]

Vanuit je Ubuntu-terminal onder WSL toont `podman run --rm alpine uname -r` `6.6.87.2-microsoft-standard-WSL2`. Een collega op een native Ubuntu-server krijgt `6.8.0-45-generic` met hetzelfde commando. Leg uit waar elke waarde vandaan komt, en wat dat betekent voor de bewering "containers zijn licht" op een Windows-werkpost.

### Vraag 12 [Analyse]

Een slecht geschreven gecontaineriseerde applicatie belandt in een oneindige lus en verbruikt al het beschikbare RAM. Verhindert de `pid`-namespace dat ze de andere containers schaadt? Wat is het juiste mechanisme om in te zetten, en wat gebeurt er als niemand het geconfigureerd heeft?

### Vraag 13 [Begrip]

In het bedrijf wordt de image van de Spring Boot-backend, gebouwd door de CI, gepromoveerd van integratie naar acceptatie en dan naar productie **zonder opnieuw gebouwd te worden**, en de acceptatieservers draaien onder Docker terwijl productie onder Podman draait. Welke eigenschappen maken die praktijk mogelijk, en welk risico neem je als je de image bij elke stap opnieuw bouwt vanuit dezelfde broncode?

### Vraag 14 [Analyse]

Een ontwikkelaar voegt `alias docker=podman` toe aan zijn `.bashrc` en beweert dat "alles wat voor Docker geschreven is, zal werken". Geef twee voorbeelden waar dat zonder voorbehoud waar is, en twee situaties waar de andere architectuur van Podman (geen daemon, rootless) het waargenomen gedrag concreet verandert.
