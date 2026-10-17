# Lab 06 — Vragen

---

### Vraag 1 [Begrip]

Een collega beweert: "Ik deed `podman stop db` en daarna `podman start db`, en mijn tabellen staan er nog. De gegevens van een container blijven dus prima bewaard, een volume is overbodig." Wat heeft hij correct waargenomen? In welke alledaagse situaties verdwijnen zijn gegevens toch?

### Vraag 2 [Diagnose]

Je start:

```bash
podman run -d --name web -p 18080:80 -v html:/usr/share/nginx/html:ro nginx:alpine
```

Je map `html/` bevat een `index.html` met "Versie 1", maar `curl localhost:18080` geeft de standaardwelkomstpagina van nginx. Leg precies uit wat er gebeurd is, waar die standaardpagina vandaan komt, en corrigeer het commando.

### Vraag 3 [Diagnose]

```bash
$ ls ~/.local/share/containers/storage/volumes/pgdata/_data
ls: cannot open directory '…/pgdata/_data': Permission denied
```

"Maar ik ben toch root in de container, en dit is mijn eigen homemap!" Leg uit waarom die weigering normaal is, van wie die bestanden zijn gezien vanaf de host, en geef het commando waarmee je ze wél kunt oplijsten.

### Vraag 4 [Voorspelling]

```bash
podman run -d --name db -e POSTGRES_PASSWORD=alpha -v pgdata:/var/lib/postgresql/data postgres:16-alpine
podman rm -f -t 0 db
podman run -d --name db -e POSTGRES_PASSWORD=bravo -v pgdata:/var/lib/postgresql/data postgres:16-alpine
```

Met welk wachtwoord kun je verbinden met de tweede container: `alpha`, `bravo`, allebei? Waarom?

### Vraag 5 [Analyse]

Kies voor elk van de volgende behoeften tussen named volume, bind mount en tmpfs, en verantwoord in één zin: (a) de broncode van een Angular-frontend tijdens de ontwikkeling; (b) de bestanden van PostgreSQL; (c) de `nginx.conf` van een reverse proxy; (d) de tussenbestanden van een PDF-conversie die tot 2 GB kunnen oplopen.

### Vraag 6 [Diagnose]

```bash
$ mkdir uitvoer
$ podman run --rm --user 1000 -v ./uitvoer:/out alpine sh -c 'id -u; echo x > /out/f'
1000
sh: can't create /out/f: Permission denied
$ ls -ln uitvoer
total 0        ← de map is van 1000:1000
```

Gebruiker 1000 kan niet schrijven in een map die van UID 1000 is. Verklaar de paradox en stel twee verschillende oplossingen voor.

### Vraag 7 [Voorspelling]

Je herhaalt het commando uit vraag 6 met `-v ./uitvoer:/out:U`. Het lukt. Wat toont `ls -ln uitvoer` op de host nu als eigenaar van de map en van het bestand? Hoe geef je de map terug aan je eigen gebruiker?

### Vraag 8 [Analyse]

Op een testserver toont `podman volume ls` veertien volumes waarvan de naam een hash van 64 tekens is. Waar komen ze vandaan? Hoe kom je per volume te weten of het nog gebruikt wordt, en door wat? Hoe voorkom je dat de lijst blijft groeien? En waarom is `podman volume prune` niet het juiste reflexantwoord?

### Vraag 9 [Begrip]

Een collega maakt elke nacht een back-up van de productiedatabase met `tar czf backup.tgz` op de map van het volume, terwijl PostgreSQL draait. De back-ups staan er, maar niemand heeft ooit een terugzetting getest. Wat is precies het risico? Welke twee manieren zijn wél correct, en welke kies je voor een dagelijkse back-up?

### Vraag 10 [Analyse]

Vergelijk `podman volume export pgdata -o pgdata.tar` met

```bash
podman run --rm -v pgdata:/data:ro -v ./:/backup alpine tar czf /backup/pgdata.tgz -C /data .
```

Wat doet het tweede commando precies, en waarom heeft het een container nodig om een map te archiveren die gewoon op jouw schijf staat? Welk van de twee werkt ook met Docker?

### Vraag 11 [Analyse]

Waarom raadt men aan om een ontsleuteld secret (private sleutel, token) in een tmpfs te zetten in plaats van in de writable layer van de container, terwijl beide verdwijnen wanneer de container verwijderd wordt? Welke prijs betaalt een tmpfs in het geheugen?

### Vraag 12 [Diagnose]

Het commando `podman run --rm -v ./conf:/etc/app:ro alpine cat /etc/app/app.yaml` werkt op jouw WSL. Op een RHEL 9-server van het bedrijf faalt het met hetzelfde bestand en dezelfde rechten: `cat: can't open '/etc/app/app.yaml': Permission denied`. Zelfs met `--user 0`. Stel de diagnose, corrigeer, en leg uit waarom de correctie onschadelijk is op Ubuntu.

### Vraag 13 [Analyse]

Het team wil **twee** containers van de Spring Boot-API achter een load balancer draaien, en wil de documenten die gebruikers uploaden bewaren in een named volume `uploads`, gemount op `/app/uploads`. Wat gaat er mislopen? Welke oplossing kiest men in het bedrijf, en wat heeft dat te maken met het principe "een container is wegwerpbaar"?
