# Lab 01 — Praktijklab: isolatie met eigen ogen zien

*Doel: elke bewering uit de theorie experimenteel nagaan. Op het einde heb je gezien dat een container een proces van je WSL-machine is, en dat de `root` van een rootless container… jij bent.*

**Vereisten** — Windows 10/11 met WSL 2 en een Ubuntu-distributie (22.04 of recenter). Voor dit lab zijn geen bestanden nodig. De getoonde uitvoer is gemaakt met Podman 5.8; vanaf Podman 4.9 zijn de commando's identiek, alleen enkele weergavedetails verschillen.

---

## Stap 0 — WSL voorbereiden en Podman installeren

In een **PowerShell**-terminal (Windows):

```powershell
wsl --version          # WSL version 2.x verwacht
wsl --list --verbose   # je Ubuntu moet VERSION 2 zijn
```

Dan in de **Ubuntu**-terminal:

```bash
cat /etc/wsl.conf
```

**Kijk na** of het bestand `[boot]` gevolgd door `systemd=true` bevat. Zo niet, voeg het toe:

```bash
printf '[boot]\nsystemd=true\n' | sudo tee /etc/wsl.conf
```

en doe vanuit PowerShell `wsl --shutdown`, open Ubuntu opnieuw. Installeer daarna Podman:

```bash
sudo apt update && sudo apt install -y podman
podman --version
```

> **Windows / WSL** — WSL 2 is een piepkleine Hyper-V-VM die in één seconde opstart en RAM deelt met Windows. Standaard heeft ze **geen** `systemd`: een historische keuze van Microsoft, en het is net `systemd` dat aan je gebruiker het recht delegeert om *cgroups* aan te maken. Zonder werken `podman run --memory` en `podman stats` niet in rootless-modus. Vandaar de stap hierboven. Je hebt Docker Desktop noch Podman Desktop nodig: Podman is hier een gewoon Ubuntu-pakket. (Gebruik je toch Podman Desktop, dan maakt `podman machine` zijn eigen WSL-distributie aan en zijn de commando's van dit lab identiek.)

---

## Stap 1 — De engine identificeren

```bash
podman version
```

**Observeer** één enkel blok, `Client: Podman Engine`, met `Version: 5.x.x` en `OS/Arch: linux/amd64`. Geen `Server`-blok.

```bash
podman info | head -n 40
podman info --format 'rootless={{.Host.Security.Rootless}} cgroups={{.Host.CgroupManager}} netwerk={{.Host.NetworkBackend}} runtime={{.Host.OCIRuntime.Name}}'
```

**Observeer** `rootless=true cgroups=systemd netwerk=netavark runtime=crun`, en in de lange uitvoer de regels `kernel: 6.6.87.2-microsoft-standard-WSL2`, `idMappings:` (we komen erop terug in stap 5) en `graphRoot: /home/<jij>/.local/share/containers/storage`.

*Uitleg.* Bij Docker ondervraagt `version` twee helften — client en daemon — en beschrijft `info` de daemon. Bij Podman is er één programma: `podman info` beschrijft wat **jouw gebruiker** kan doen. De `graphRoot` in je `home` bevestigt het: de images zitten niet in `/var/lib`, ze zijn van jou.

---

## Stap 2 — De eerste container, en waar hij gebleven is

```bash
podman run alpine echo "hallo vanuit de container"
```

**Observeer** eerst `Resolved "alpine" as an alias (/etc/containers/registries.conf.d/000-shortnames.conf)`, dan `Trying to pull docker.io/library/alpine:latest...`, regels `Copying blob`, `Writing manifest`, de getoonde boodschap… en dan meteen de prompt terug.

> **Podman** — Docker vult `alpine` stilzwijgend aan tot `docker.io/library/alpine`. Podman weigert te gokken: het raadpleegt een lijst gekende aliassen (`alpine`, `nginx`, `debian`, `node`, `postgres`…) en voor een onbekende naam **vraagt** het je op welke registry te zoeken — of het faalt als er geen terminal beschikbaar is. Daarom schrijven Dockerfiles en scripts in bedrijven altijd de volledige naam: `docker.io/library/eclipse-temurin:21-jre`. Neem die gewoonte nu al aan.

```bash
podman ps
podman ps -a
```

**Observeer** dat `podman ps` **niets** toont, maar dat `podman ps -a` de container toont, met een willekeurige naam (`trusting_sanderson`…), de image onder haar volledige naam `docker.io/library/alpine:latest`, en de status `Exited (0)`.

```bash
podman run --rm alpine echo "deze laat geen spoor na"
podman ps -a
```

**Observeer** dat er geen nieuwe container bijkomt: `--rm` verwijdert de container bij het afsluiten.

*Uitleg.* Een container leeft precies zo lang als zijn hoofdproces. `echo` schreef één regel en stopte: de container stierf mee, maar wordt daarom niet verwijderd — hij blijft als een inspecteerbaar lijk achter. `podman ps` toont alleen draaiende containers.

---

## Stap 3 — De kernel is die van de host (en de host is WSL)

```bash
uname -r
podman run --rm alpine uname -r
podman run --rm debian uname -r
```

**Observeer** dat de **drie** commando's dezelfde waarde tonen, bijvoorbeeld `6.6.87.2-microsoft-standard-WSL2` — terwijl Ubuntu, Alpine en Debian drie verschillende systemen zijn.

```bash
podman run --rm alpine cat /etc/os-release | head -n 2
podman run --rm debian cat /etc/os-release | head -n 2
```

**Observeer** deze keer twee verschillende resultaten: `Alpine Linux` en `Debian GNU/Linux`.

*Uitleg.* Het bewijs is geleverd: de image brengt de *userland* (bestanden, binaries, bibliotheken), de kernel komt van de host en wordt nooit gedupliceerd. En die host is niet Windows: het achtervoegsel `microsoft-standard-WSL2` is de handtekening van de Linux-kernel die Microsoft voor WSL compileert. Je containers draaien in die VM.

> **Linux** — `/etc/os-release` is een gewoon tekstbestand dat elke distributie installeert om zich voor te stellen. `uname -r` daarentegen is een **systeemaanroep**: het antwoord komt van de kernel. Daarom verschilt het eerste van container tot container en het tweede niet.

---

## Stap 4 — Het proces van beide kanten bekijken

Start een container die blijft draaien:

```bash
podman run -d --name waker alpine sleep 600
podman ps
```

**Observeer** de status `Up`, de naam `waker`, en het commando `sleep 600`.

Zicht **van binnenuit**:

```bash
podman exec waker ps -o pid,ppid,comm
```

**Observeer** een minuscule lijst: `sleep` heeft **PID 1**, en je `ps` PID 2.

Zicht **vanaf de host**:

```bash
ps -ef | grep "[s]leep 600"
podman inspect --format '{{.State.Pid}}' waker
```

**Observeer** dat hetzelfde proces op de host bestaat, eigendom van **jouw gebruiker**, met een gewone PID (bijvoorbeeld `1854`), en dat `podman inspect` je precies die PID geeft.

```bash
podman top waker
```

**Observeer** `USER root`, `PID 1`, `COMMAND sleep 600`: het "containerzicht" op hetzelfde proces, gereconstrueerd door Podman.

*Uitleg.* Eén en hetzelfde proces, twee nummeringen. Binnenin laat de `pid`-namespace het geloven dat het het eerste proces van het systeem is; buiten is het maar een proces tussen honderden, en het is van jou. Dat is het hele idee van een container.

Ga na dat die isolatie kan worden weggenomen:

```bash
podman run --rm --pid=host alpine ps -o pid,comm | head -n 8
```

**Observeer** de processen van **je WSL** (`init`, `systemd`, `conmon`…), opgelijst vanuit een container.

*Uitleg.* Isolatie is een optie, geen intrinsieke eigenschap. Daarom zijn `--pid=host` en `--privileged` standaard verboden in productie. Merk terloops `conmon` op: dat is de kleine toezichthouder die Podman achter elke container laat, aangezien er geen daemon is om dat te doen.

---

## Stap 5 — De root die er geen is (rootless)

```bash
podman exec waker id
```

**Observeer** `uid=0(root) gid=0(root)`: in de container draait `sleep` als root.

```bash
podman top waker user,huser,pid,hpid,comm
```

**Observeer**:

```
USER        HUSER       PID         HPID        COMMAND
root        1000        1           1854        sleep 600
```

`USER` is de identiteit gezien vanuit de container, `HUSER` de echte identiteit op de host: `1000`, dat ben jij (`id -u` om na te gaan).

```bash
podman unshare cat /proc/self/uid_map
```

**Observeer** een vertaaltabel van dit type:

```
         0       1000          1
         1     100000      65536
```

*Uitleg.* Dit is de `user`-namespace in actie. Regel 1: UID `0` van de container **is** jouw UID `1000`. Regel 2: de UID's `1` tot `65536` van de container worden geprojecteerd op een "reserve"-bereik van UID's (`100000`+, vastgelegd in `/etc/subuid`) dat niemand anders gebruikt. De "root" van de container heeft op de host dus alleen jouw rechten. Een gecompromitteerde container kan geen root worden op je WSL: er valt niets te escaleren.

> **Beveiliging** — Bij Docker draait de daemon als root en is een container-`root`, tenzij speciaal geconfigureerd, de echte root van de host. De isolatie steunt dan uitsluitend op de `pid`/`mnt`/`net`-namespaces en op de weggenomen *capabilities*. Rootless Podman voegt een laag toe die Docker standaard niet heeft: zelfs als al de rest bezwijkt, is de aanvaller een gewone gebruiker.

---

## Stap 6 — Onveranderlijke image, wegwerpbare container

```bash
podman run -d --name c1 alpine sleep 600
podman run -d --name c2 alpine sleep 600
podman exec c1 sh -c 'echo "gegevens van c1" > /merk.txt'
```

Ga na dat de schrijfacties geïsoleerd zijn:

```bash
podman exec c1 cat /merk.txt      # toont: gegevens van c1
podman exec c2 cat /merk.txt      # cat: can't open '/merk.txt': No such file or directory
```

Ga na dat de image zelf niet bewogen is:

```bash
podman run --rm alpine ls /merk.txt    # No such file or directory
```

Meet die laag:

```bash
podman ps -s --format 'table {{.Names}}\t{{.Size}}'
```

**Observeer** een grootte als `11.4kB (virtual 8.72MB)`: `virtual` is image + laag, de eerste waarde is wat de container **zelf** verbruikt — enkele kilobytes metadata, plus jouw bestand.

Vernietig ten slotte en begin opnieuw:

```bash
podman rm -f -t 0 c1
podman run -d --name c1 alpine sleep 600
podman exec c1 ls /merk.txt        # No such file or directory
```

*Uitleg.* `podman rm` vernietigt de container **én** zijn schrijflaag. De nieuwe `c1` vertrekt opnieuw van de exacte toestand van de image. Alle gegevens die bewaard moeten blijven, moeten de container verlaten: dat is het onderwerp van lab 06.

> **Podman** — Waarom `-t 0`? `podman rm -f` begint met een beleefde stop (`SIGTERM`), wacht **10 seconden** en doodt dan pas. Docker doodt meteen. Omdat `sleep` `SIGTERM` negeert (lab 03), zou je zonder `-t 0` tien seconden zitten kijken naar een waarschuwing `StopSignal SIGTERM failed to stop container … resorting to SIGKILL`. Dat is geen bug: het is Podman dat je zegt dat je applicatie niet netjes stopt.

---

## Stap 7 — Cgroups, of de verbruikslimiet

```bash
podman run -d --name limiet --memory=128m --memory-swap=128m alpine sleep 600
podman stats --no-stream limiet
```

**Observeer** de kolom `MEM USAGE / LIMIT`: `471kB / 134.2MB`, en niet het totale RAM van je machine.

Vergelijk met een container zonder limiet:

```bash
podman stats --no-stream waker
```

**Observeer** dat de getoonde limiet het totale RAM is… **van de WSL-VM**, bijvoorbeeld `7.7GB` op een pc met 16 GB.

*Uitleg.* Zonder `--memory` kan een container al het beschikbare geheugen verbruiken. De namespace beschermt hier tegen niets: de cgroup begrenst. Als deze stap faalt met `OCI runtime error: … cgroup …`, dan is `systemd` niet actief in je WSL (stap 0).

> **Windows / WSL** — WSL 2 ziet standaard slechts **50 % van het RAM** van Windows (en hoogstens 8 GB op oudere versies). Dat is instelbaar in `%UserProfile%\.wslconfig` (`[wsl2]` en dan `memory=12GB`). Wanneer een container "geheugen tekortkomt" op een Windows-werkpost, is de limiet die telt vaak die, niet die van de container.

---

## Stap 8 — `inspect`, de bron van waarheid

```bash
podman inspect waker | head -n 30
```

Dat is breedsprakig: richt je op wat je interesseert met een *Go-template*.

```bash
podman inspect --format '{{.State.Status}}' waker
podman inspect --format '{{.Config.Image}}' waker
podman inspect --format '{{json .Config.Cmd}}' waker
podman inspect --format '{{.NetworkSettings.IPAddress}}' waker
```

**Observeer** respectievelijk `running`, `docker.io/library/alpine:latest`, `["sleep","600"]`… en **een lege regel** voor het IP-adres.

```bash
podman exec waker ip -4 addr show eth0
```

**Observeer** dat de container toch een interface `eth0` heeft, met **hetzelfde IP-adres als je WSL** (`172.2x.x.x`).

*Uitleg.* In rootless-modus mag een gewone gebruiker geen netwerkbrug aanmaken. Podman gebruikt daarom `pasta`, een vertaler in userspace die het adres van de host in de container *kopieert*; er is geen "container-IP" om te tonen. Dat wordt een thema van lab 07. Onthoud voorlopig dat de lege waarde geen fout is, en dat `--network podman` je een echte brug zou geven met een IP `10.88.0.x`:

```bash
podman run -d --network podman --name brug alpine sleep 600
podman inspect --format '{{.NetworkSettings.Networks.podman.IPAddress}}' brug
```

**Observeer** `10.88.0.2`. Vergelijk met de metadata van de **image**:

```bash
podman image inspect --format '{{json .Config.Cmd}}' alpine
podman image inspect --format '{{.Architecture}}/{{.Os}}' alpine
```

**Observeer** dat ook de image een standaardcommando draagt (`["/bin/sh"]`), dat je `sleep 600` bij de `run` overschreven heeft, en `amd64/linux`.

*Uitleg.* `podman inspect` werkt op **alle** objecten (container, image, volume, netwerk) en geeft de echte toestand, zonder opmaak. Wanneer documentatie en werkelijkheid uiteenlopen, heeft `inspect` gelijk.

---

## Stap 9 — De CLI, lange vorm, korte vorm… en `docker`

```bash
podman container ls -a
podman ps -a
podman image ls
podman images
```

**Observeer** twee aan twee identieke uitvoer.

```bash
podman container ls --format 'table {{.Names}}\t{{.Image}}\t{{.Status}}'
```

Doe je nu voor als Docker:

```bash
alias docker=podman
docker ps
docker images
```

**Observeer** dat alles werkt. Om de alias permanent te maken: `echo 'alias docker=podman' >> ~/.bashrc`. Op Ubuntu doet het pakket `podman-docker` hetzelfde (het levert een `docker`-binary dat `podman` aanroept).

*Uitleg.* `--format` aanvaardt een Go-template en maakt uitvoer bruikbaar in scripts — veel betrouwbaarder dan de standaardtabel met `awk` versnijden. En de alias: CLI-compatibiliteit is een belofte van Podman, en het is wat je toelaat eender welke Docker-tutorial te volgen.

---

## Opruimen

```bash
podman rm -f -t 0 waker c1 c2 limiet brug
podman ps -a
```

De `Exited`-container van stap 2 blijft over. Verwijder hem bij naam:

```bash
podman ps -a --filter status=exited --format '{{.Names}}'
podman rm <naam>
```

En als je de ruimte van de Debian-image wilt terugwinnen, die niet meer van pas komt:

```bash
podman images
podman rmi debian          # alpine houden we voor de volgende labs
```

> **Valkuil** — je zult overal `podman container prune`, `podman image prune -a` en `podman system prune -a` tegenkomen. Die commando's verwijderen niet "wat je net gedaan hebt" maar **alles wat niet in gebruik is**: de images en containers van je andere projecten gaan mee. Verwijder altijd bij naam. We behandelen `prune` grondig in lab 10.

---

## Wat je nu moet kunnen beweren

- De kernel die in een container getoond wordt, is die van de host — hier die van WSL 2.
- Het proces van een container bestaat in de `ps` van de host, onder **jouw** gebruiker — je hebt het gezien, met zijn PID.
- De `root` van een rootless container is een projectie van jouw UID: `podman unshare cat /proc/self/uid_map` bewijst het.
- Een schrijfactie in een container bereikt de image niet, en de andere containers ook niet.
- `podman rm` vernietigt gegevens; `podman stop` niet. `podman rm -f` wacht 10 s zonder `-t 0`.
- Zonder `--memory` is de enige limiet het RAM van de WSL-VM.
- `podman inspect --format` is je eerste diagnosereflex — en een leeg IP in rootless-modus is normaal.
