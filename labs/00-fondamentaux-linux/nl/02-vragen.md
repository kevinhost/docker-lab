# Labo 00 — Vragen

*Antwoord zonder de theorie te herlezen. Eén tot vijf zinnen volstaan; wat telt is de redenering, niet de woordenschat.*

---

### Vraag 1 [Begrip]

Een binary gecompileerd voor Linux (bijvoorbeeld `nginx`) werkt identiek op Ubuntu, Debian en Alpine, maar helemaal niet op Windows zonder WSL. Leg uit wat die binary van zijn systeem verwacht, en waarom de distributie er niet toe doet terwijl de kernel dat wél doet.

### Vraag 2 [Analyse]

Je start `sleep 300 &` in een terminal en sluit daarna die terminal. Even later toont `ps -ef` dat het `sleep`-proces nog altijd bestaat, maar dat zijn PPID nu `1` is. Wat is er gebeurd, en waarom heeft het systeem dit mechanisme nodig?

### Vraag 3 [Diagnose]

Een collega toont je dit:

```
$ ./deploy.sh
bash: ./deploy.sh: Permission denied
$ echo $?
126
```

Het bestand bestaat en hij is er eigenaar van. Geef de exacte oorzaak, het commando dat ze bevestigt, het commando dat ze verhelpt — en een tweede manier om het script te starten zonder ook maar iets te verhelpen.

### Vraag 4 [Voorspelling]

Voorspel de twee regels die deze reeks toont, en verklaar het verschil:

```bash
MSG=hallo
bash -c 'echo 1: $MSG'
export MSG
bash -c 'echo 2: $MSG'
```

### Vraag 5 [Diagnose]

In een beheerscript vind je `echo $?` dat `137` toont, net na het abrupte stoppen van een Java-dienst. Ontleed dat getal, zeg wat er met het proces gebeurd is, en waarom precies die code beroemd is in de containerwereld.

### Vraag 6 [Analyse]

Veel gehaaste beheerders doen systematisch `kill -9` in plaats van `kill`. Leg het verschil in mechanisme uit tussen beide, wat een applicatie van het type databank concreet verliest in het tweede geval, en het verband met de manier waarop Docker een container stopt (`docker stop`).

### Vraag 7 [Diagnose]

Bekijk:

```
$ cat /etc/shadow
cat: /etc/shadow: Permission denied
$ ls -l /etc/shadow
-rw-r----- 1 root shadow 652 mrt 31 13:31 /etc/shadow
$ sudo cat /etc/shadow    # werkt
```

Leg, op basis van de regel van `ls -l`, precies uit waarom de eerste `cat` faalt en waarom de tweede lukt. Wie zou dit bestand kunnen lezen zonder `sudo`?

### Vraag 8 [Voorspelling]

Wat bevat het bestand `resultaat.txt` en wat verschijnt er op het scherm na dit commando, wetende dat `/onbekende-datum` niet bestaat?

```bash
ls /etc/hostname /onbekende-datum > resultaat.txt 2> fouten.txt
```

En wat zou `2>&1`, geplaatst na `> resultaat.txt`, veranderen?

### Vraag 9 [Analyse]

`ss -tlnp` op een server toont deze twee regels:

```
LISTEN 0  511      127.0.0.1:6379   0.0.0.0:*   users:(("redis-server",pid=812,fd=6))
LISTEN 0  511        0.0.0.0:8080   0.0.0.0:*   users:(("java",pid=944,fd=23))
```

Wat is het verschil in bereik tussen deze twee diensten? Welke kun je bereiken vanaf een andere machine in het netwerk? Waarom wordt dit detail belangrijk wanneer je containerpoorten gaat publiceren?

### Vraag 10 [Begrip]

Jouw gebruiker (UID 1000) start `python3 -m http.server 80` en krijgt `PermissionError: [Errno 13] Permission denied`, terwijl poort 8080 werkt. Leg de regel uit die hier speelt, haar historische bestaansreden, en het directe gevolg voor Podman rootless.

### Vraag 11 [Analyse]

`ls /proc` toont honderden mappen, en toch toont `df -h` geen enkele schijfruimte verbruikt door `/proc`; `findmnt -t proc` onthult een bestandssysteem van het type `proc`. Leg uit wat `/proc` werkelijk is, waar zijn "bestanden" vandaan komen, en geef een voorbeeld van informatie die je er gaat zoeken.

### Vraag 12 [Diagnose]

Op een vers geïnstalleerde machine heeft een collega een tool gekopieerd naar `~/tools/mijntool`, met `ls` gecontroleerd dat hij wel degelijk uitvoerbaar is, maar hij krijgt:

```
$ mijntool
bash: mijntool: command not found
$ echo $?
127
```

Leg uit hoe de shell `mijntool` gezocht heeft, waarom hij hem niet vond, en geef twee duurzame manieren (en één onmiddellijke) om het commando bruikbaar te maken.

### Vraag 13 [Analyse]

De "12-factor"-methodologie legt op om een applicatie te configureren via **omgevingsvariabelen** in plaats van via handmatig gewijzigde bestanden. Leg, op basis van wat je weet over de overerving ouder → kind en de levenscyclus van een proces, uit waarom die keuze perfect past bij wegwerpbare en herstartbare processen — zoals jouw Spring Boot-containers in labo 08 zullen zijn.
