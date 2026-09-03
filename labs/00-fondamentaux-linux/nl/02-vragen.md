# Labo 00 — Vragen

*Antwoord zonder de theorie erbij te nemen. Eén tot vijf zinnen volstaan — het gaat om de redenering, niet om de woordenschat.*

---

### Vraag 1 [Begrip]

Een binary die voor Linux is gecompileerd (bijvoorbeeld `nginx`) draait identiek op Ubuntu, Debian en Alpine, maar helemaal niet op Windows zonder WSL. Wat heeft die binary eigenlijk nodig van zijn systeem? Waarom maakt de distributie niets uit, terwijl de kernel alles uitmaakt?

### Vraag 2 [Analyse]

Je start `sleep 300 &` in een terminal en sluit daarna die terminal. Even later toont `ps -ef` dat het `sleep`-proces nog bestaat — maar zijn PPID is nu `1`. Wat is er gebeurd, en waarom heeft het systeem dit mechanisme nodig?

### Vraag 3 [Diagnose]

Een collega toont je dit:

```
$ ./deploy.sh
bash: ./deploy.sh: Permission denied
$ echo $?
126
```

Het bestand bestaat en de collega is er eigenaar van. Geef de exacte oorzaak, het commando dat ze bevestigt, het commando dat ze oplost — en een tweede manier om het script te starten zonder ook maar iets aan te passen.

### Vraag 4 [Voorspelling]

Voorspel de twee regels die deze reeks afdrukt, en verklaar het verschil:

```bash
MSG=hallo
bash -c 'echo 1: $MSG'
export MSG
bash -c 'echo 2: $MSG'
```

### Vraag 5 [Diagnose]

In een beheerscript zie je `echo $?` het getal `137` afdrukken, net nadat een Java-dienst abrupt gestopt is. Ontleed dat getal, zeg wat er met het proces gebeurd is, en leg uit waarom net deze code zo berucht is in de containerwereld.

### Vraag 6 [Analyse]

Heel wat ongeduldige beheerders grijpen meteen naar `kill -9` in plaats van `kill`. Leg uit hoe de twee technisch verschillen, wat een databank concreet verliest in het tweede geval, en wat het verband is met de manier waarop Docker een container stopt (`docker stop`).

### Vraag 7 [Diagnose]

Bekijk dit:

```
$ cat /etc/shadow
cat: /etc/shadow: Permission denied
$ ls -l /etc/shadow
-rw-r----- 1 root shadow 652 mrt 31 13:31 /etc/shadow
$ sudo cat /etc/shadow    # werkt
```

Leg aan de hand van de `ls -l`-regel precies uit waarom de eerste `cat` faalt en de tweede lukt. Wie zou dit bestand kunnen lezen zonder `sudo`?

### Vraag 8 [Voorspelling]

`/onbestaand-pad` bestaat niet. Wat komt er na dit commando in `resultaat.txt` terecht, en wat verschijnt er op het scherm?

```bash
ls /etc/hostname /onbestaand-pad > resultaat.txt 2> fouten.txt
```

En wat zou er veranderen als je `2>&1` toevoegt na `> resultaat.txt`?

### Vraag 9 [Analyse]

`ss -tlnp` op een server toont deze twee regels:

```
LISTEN 0  511      127.0.0.1:6379   0.0.0.0:*   users:(("redis-server",pid=812,fd=6))
LISTEN 0  511        0.0.0.0:8080   0.0.0.0:*   users:(("java",pid=944,fd=23))
```

Hoe verschillen deze twee diensten in bereik? Welke kun je bereiken vanaf een andere machine in het netwerk? En waarom wordt dit detail belangrijk zodra je containerpoorten gaat publiceren?

### Vraag 10 [Begrip]

Jouw gebruiker (UID 1000) start `python3 -m http.server 80` en krijgt `PermissionError: [Errno 13] Permission denied` — poort 8080 werkt nochtans prima. Leg de regel uit die hier speelt, waarom die historisch bestaat, en wat hij betekent voor rootless Podman.

### Vraag 11 [Analyse]

`ls /proc` toont honderden mappen, en toch meldt `df -h` geen enkele schijfruimte voor `/proc`; `findmnt -t proc` onthult een bestandssysteem van het type `proc`. Wat is `/proc` nu echt? Waar komen zijn "bestanden" vandaan? Geef één voorbeeld van informatie die je er gaat zoeken.

### Vraag 12 [Diagnose]

Op een vers geïnstalleerde machine heeft een collega een tool naar `~/tools/mijntool` gekopieerd en met `ls` gecontroleerd dat hij uitvoerbaar is. Toch:

```
$ mijntool
bash: mijntool: command not found
$ echo $?
127
```

Leg uit hoe de shell naar `mijntool` heeft gezocht en waarom dat mislukte. Geef daarna twee blijvende oplossingen — en één onmiddellijke noodoplossing.

### Vraag 13 [Analyse]

De "12-factor"-methodologie schrijft voor dat je een applicatie configureert via **omgevingsvariabelen**, niet via handmatig aangepaste bestanden. Leg met wat je weet over de overerving van ouder naar kind en over de levenscyclus van een proces uit waarom die aanpak zo goed past bij wegwerpprocessen die je zo weer herstart — precies wat jouw Spring Boot-containers in labo 08 zullen zijn.
