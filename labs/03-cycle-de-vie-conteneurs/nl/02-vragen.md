# Lab 03 — Vragen

---

### Vraag 1 [Begrip]

`podman run alpine` geeft je meteen de prompt terug, `podman run nginx` blokkeert de terminal, en `podman run -it alpine sh` opent een shell. Verklaar deze drie gedragingen met **één en dezelfde regel**.

### Vraag 2 [Diagnose]

Een ontwikkelaar zet de interne API in een container en stopt dit opstartscript in de image:

```sh
#!/bin/sh
java -jar /app/api.jar &
echo "API gestart"
```

De container toont netjes "API gestart" en stopt daarna onmiddellijk met code `0`. Leg precies uit wat er gebeurt, en corrigeer het script.

### Vraag 3 [Analyse]

Je voert `podman run -d --name wacht alpine sleep 300` uit, en daarna `podman stop wacht`. Het commando heeft **10 seconden** nodig om terug te keren, toont de waarschuwing `StopSignal SIGTERM failed to stop container wacht in 10 seconds, resorting to SIGKILL`, en de container eindigt met code `137`. Toch heeft `sleep` niets op te slaan. Waarom stopte het niet onmiddellijk, en waarom `137` in plaats van `143`?

### Vraag 4 [Analyse]

Neem vraag 3 opnieuw, maar nu met `podman run -d --init --name wacht alpine sleep 300`. Deze keer keert de `stop` **onmiddellijk** terug en is de exitcode `143`. Wat heeft `--init` precies veranderd? Wat zou je zien in `podman exec wacht ps`?

### Vraag 5 [Begrip]

Wat is het verschil tussen `-i` en `-t`? Wat gebeurt er concreet als je `podman run -t alpine sh` start (zonder `-i`) en dan `ls` typt? En bij `podman run -i alpine sh` (zonder `-t`)?

### Vraag 6 [Diagnose]

Een collega start `podman attach mijn-api` om de logs te bekijken, drukt op `Ctrl+C` om eruit te gaan… en de productie ligt plat. Leg uit wat er gebeurd is, en geef de twee correcte manieren om te doen wat hij eigenlijk wilde.

### Vraag 7 [Analyse]

Na een incident toont `podman ps -a`:

```
NAMES     STATUS
api       Exited (137) 4 minutes ago
worker    Exited (143) 4 minutes ago
batch     Exited (127) 4 minutes ago
```

Zeg voor elk van de drie wat er hoogstwaarschijnlijk gebeurd is, en welk commando je daarna zou uitvoeren om dat te bevestigen.

### Vraag 8 [Analyse]

Je Spring Boot-applicatie schrijft haar logs naar `/var/log/api/application.log` via `logging.file.name`, net zoals op de oude servers. `podman logs api` geeft niets terug. Leg uit waarom — noem daarbij het proces dat bij Podman de logs opvangt — en leg uit waarom de "oplossing" om die map op de host te mounten een slecht antwoord blijft.

### Vraag 9 [Begrip]

`podman stop` en daarna `podman start` op een PostgreSQL-container: blijven de gegevens bewaard? En na `podman rm` gevolgd door een nieuwe `podman run`? Verklaar het verschil aan de hand van het onderliggende mechanisme.

### Vraag 10 [Analyse]

Een beheerder die Docker gewend is, voert op een Podman-server `podman run -d --restart=always --name api mijn-api:1.0` uit. Hij controleert dat de container inderdaad herstart wanneer hij hem doodt, en reboot daarna de server voor een kernelupdate. Na de reboot is `podman ps` leeg. Leg uit waarom, en beschrijf hoe je bij Podman wél garandeert dat een container bij het booten start.

### Vraag 11 [Diagnose]

Een container met `--restart=on-failure:5` is vijf keer herstart en daarna definitief gestopt. Waar vind je de logs van de **eerste** poging, die met de oorspronkelijke oorzaak? En wat gebeurt er als je `podman restart` uitvoert voordat je gekeken hebt?

### Vraag 12 [Analyse]

Een container gebruikt één core voor 100% en reageert niet meer. Je wilt weten wat hij aan het doen is voordat je hem doodt. Rangschik deze commando's van minst naar meest ingrijpend, en zeg wat elk ervan je leert: `podman logs`, `podman top`, `podman stats`, `podman exec`, `podman inspect`.

### Vraag 13 [Begrip]

Waarom zetten we de Spring Boot-API en haar PostgreSQL-database niet in dezelfde container, ook al zou dat eenvoudiger te starten zijn? Geef drie concrete gevolgen, op basis van wat je over de levenscyclus weet.

### Vraag 14 [Analyse]

`podman run --rm` wordt aanbevolen voor eenmalige commando's, maar **afgeraden** voor een dienst in productie — Podman weigert het trouwens te combineren met `--restart`. Leg de redenering in beide gevallen uit: wat verlies je precies wanneer een productiecontainer bij het afsluiten verdwijnt, en waarom is die combinatie tegenstrijdig?
