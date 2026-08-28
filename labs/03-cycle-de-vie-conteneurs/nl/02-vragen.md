# Lab 03 — Vragen

---

### Vraag 1 [Begrip]

`podman run alpine` geeft meteen de hand terug, `podman run nginx` blokkeert de terminal, en `podman run -it alpine sh` opent een shell. Verklaar deze drie gedragingen met **één en dezelfde regel**.

### Vraag 2 [Diagnose]

Een ontwikkelaar containeriseert de eigen API en schrijft in zijn image een opstartscript:

```sh
#!/bin/sh
java -jar /app/api.jar &
echo "API gestart"
```

De container toont wel degelijk "API gestart" en stopt dan meteen met code `0`. Leg precies uit wat er gebeurt, en corrigeer het script.

### Vraag 3 [Analyse]

Je start `podman run -d --name wacht alpine sleep 300`, en dan `podman stop wacht`. Het commando doet er **10 seconden** over om terug te komen, toont een waarschuwing `StopSignal SIGTERM failed to stop container wacht in 10 seconds, resorting to SIGKILL`, en de container eindigt met code `137`. Nochtans heeft `sleep` niets te bewaren. Waarom stopte het niet onmiddellijk, en waarom `137` in plaats van `143`?

### Vraag 4 [Analyse]

Herneem vraag 3, maar met `podman run -d --init --name wacht alpine sleep 300`. De `stop` komt deze keer **onmiddellijk** terug en de exitcode is `143`. Wat heeft `--init` precies veranderd? Wat zou je zien in `podman exec wacht ps`?

### Vraag 5 [Begrip]

Maak het onderscheid tussen `-i` en `-t`. Wat gebeurt er concreet als je `podman run -t alpine sh` (zonder `-i`) start en dan `ls` typt? En `podman run -i alpine sh` (zonder `-t`)?

### Vraag 6 [Diagnose]

Een collega start `podman attach mijn-api` om de logs te lezen, drukt op `Ctrl+C` om eruit te gaan… en productie valt uit. Leg uit wat er gebeurd is, en geef de twee correcte manieren om zijn oorspronkelijke doel te bereiken.

### Vraag 7 [Analyse]

Na een incident toont `podman ps -a`:

```
NAMES     STATUS
api       Exited (137) 4 minutes ago
worker    Exited (143) 4 minutes ago
batch     Exited (127) 4 minutes ago
```

Zeg voor elk van de drie wat er hoogstwaarschijnlijk gebeurd is en welk commando je vervolgens zou uitvoeren om het te bevestigen.

### Vraag 8 [Analyse]

Je Spring Boot-applicatie schrijft haar logs naar `/var/log/api/application.log` dankzij `logging.file.name`, zoals op de oude servers. `podman logs api` geeft niets terug. Leg uit waarom — en noem het proces dat bij Podman de logs opvangt — en zeg waarom de "oplossing" om die map op de host te mounten een slecht antwoord blijft.

### Vraag 9 [Begrip]

`podman stop` en dan `podman start` op een PostgreSQL-container: blijven de gegevens bewaard? En na `podman rm` en een nieuwe `podman run`? Leg het verschil uit met het onderliggende mechanisme.

### Vraag 10 [Analyse]

Een beheerder die Docker gewoon is, start op een Podman-server `podman run -d --restart=always --name api mijn-api:1.0`, controleert dat de container inderdaad herstart wanneer hij hem doodt, en herstart dan de server voor een kernelupdate. Bij terugkeer is `podman ps` leeg. Leg uit waarom, en zeg wat de Podman-manier is om de herstart bij het booten te garanderen.

### Vraag 11 [Diagnose]

Een container met `--restart=on-failure:5` is vijf keer herstart en dan definitief gestopt. Waar vind je de logs van de **eerste** poging, die met de oorspronkelijke oorzaak? Wat gebeurt er als je `podman restart` doet voor je gekeken hebt?

### Vraag 12 [Analyse]

Een container verbruikt 100 % van een core en reageert niet meer. Je wilt weten wat hij doet voor je hem doodt. Rangschik deze commando's van minst naar meest ingrijpend, en zeg wat elk je leert: `podman logs`, `podman top`, `podman stats`, `podman exec`, `podman inspect`.

### Vraag 13 [Begrip]

Waarom zetten we de Spring Boot-API en haar PostgreSQL-database niet in dezelfde container, terwijl dat eenvoudiger te starten zou zijn? Geef drie concrete gevolgen, steunend op wat je weet over de levenscyclus.

### Vraag 14 [Analyse]

`podman run --rm` wordt aanbevolen voor eenmalige commando's, maar **afgeraden** voor een dienst in productie — en Podman weigert het trouwens te combineren met `--restart`. Leg de redenering in beide gevallen uit: wat verliest men precies wanneer een productiecontainer bij het afsluiten verdwijnt, en waarom is de combinatie tegenstrijdig?
