# Lab 09 — Vragen

---

### Vraag 1 [Begrip]

Een collega heeft een script `starten.sh` van dertig regels `podman network create`, `podman volume create` en `podman run`, en een `stoppen.sh` dat het omgekeerde doet. "Het werkt, waarom Compose?" Geef drie dingen die `podman compose up` / `down` weten en zijn scripts niet, zonder het over de lengte te hebben.

### Vraag 2 [Diagnose]

Het bestand `.env` naast `compose.yaml` bevat `APP_MESSAGE=hallo vanuit dotenv`. Na `podman compose up -d` geeft `curl localhost:18080/api/` nog altijd het standaardbericht. Toch meldt `podman compose config` geen enkele fout. Leg uit wat `.env` werkelijk doet, en waar `APP_MESSAGE` gedeclareerd had moeten worden.

### Vraag 3 [Voorspelling]

Twee versies van de afhankelijkheid van `api` op `db`:

```yaml
depends_on: [db]
```
```yaml
depends_on:
  db:
    condition: service_healthy
```

Beschrijf voor een echte Spring Boot-API wat er bij `up -d` gebeurt in elk geval (volgorde, logs, eindtoestand), en waarom de tweede vorm een `healthcheck`-blok op `db` vereist.

### Vraag 4 [Diagnose]

```yaml
api:
  image: localhost/api:1.0
  healthcheck:
    test: ["CMD", "curl", "-f", "http://localhost:8080/actuator/health"]
    interval: 5s
    retries: 3
```

Na dertig seconden toont `podman compose ps` `api` als `(unhealthy)` en is `web` nooit gestart, terwijl `curl localhost:18080` werkte vóór het toevoegen van de healthcheck. Stel de diagnose met één commando, corrigeer, en zeg waarom de image de oorzaak is.

### Vraag 5 [Analyse]

Vergelijk in `compose.yaml` `- pgdata:/var/lib/postgresql/data` (met `volumes: pgdata:` onderaan) met `- ./data:/var/lib/postgresql/data`: wie maakt de map aan, van wie zijn de bestanden in rootless, wat doet `down -v` in elk geval, en welke kies je voor de database van de stack?

### Vraag 6 [Voorspelling]

Een ontwikkelaar kloont het project in `~/werk/stack-v2/` in plaats van `~/werk/stack/`, start `podman compose up -d`, en ziet een **lege** database: "Compose heeft mijn gegevens verloren!" Het bestand heeft geen sleutel `name:`. Verklaar, toon met `podman volume ls` wat er gebeurd is, en geef twee manieren om het probleem te vermijden.

### Vraag 7 [Diagnose]

```bash
$ podman compose -f compose.yaml -f compose.prod.yaml up -d
$ podman compose exec api env | grep APP_PROFILE
APP_PROFILE=dev
$ podman exec stack_api_1 env | grep APP_PROFILE
APP_PROFILE=prod
```

Twee commando's, twee antwoorden voor dezelfde container. Welk zegt de waarheid, waar komt het andere vandaan, en hoe vermijd je de verwarring?

### Vraag 8 [Analyse]

`compose.prod.yaml` zet `restart: unless-stopped` op de drie diensten. Wat gebeurt er op een Linux-server met Docker na een herstart van de machine? En op jouw WSL met rootless Podman, na `wsl --shutdown`? Verklaar het verschil en wat je met Podman in de plaats moet gebruiken.

### Vraag 9 [Begrip]

`podman compose up -d --scale api=2` maakt `stack_api_1` en `stack_api_2` aan. Hoe verdeelt `web` de verzoeken over de twee, zonder enige configuratie? Waarom zou `--scale web=2` mislukken? En wat moet je doen vóór `podman compose down` met podman-compose?

### Vraag 10 [Diagnose]

```bash
$ podman compose up -d
Error: creating container storage: the container name "stack_db_1" is already in use by 3e5c2093…
```

Waar komt die container vandaan, waarom hergebruikt `up` hem niet, en wat is de herstelreeks zonder het volume te verliezen?

### Vraag 11 [Analyse]

In `compose.yaml` krijgt de database haar wachtwoord via `secrets: [db_password]` en `POSTGRES_PASSWORD_FILE`, waarbij het secret gedeclareerd is als `file: ./db_password.txt`. Vergelijk met `environment: POSTGRES_PASSWORD: S3cr3t`: waar verschijnt de waarde in elk geval (`podman compose config`, `podman inspect`, Git)? Wat moet er met `db_password.txt` gebeuren, en wat verandert `external: true`?

### Vraag 12 [Analyse]

Koppel elk element van onze `compose.yaml` aan zijn Kubernetes-equivalent, in één regel elk: een `service` met `image`, `ports`, het volume `pgdata`, de `healthcheck`, de `depends_on`, het impliciete netwerk, `env_file`, `secrets`. Welk heeft **geen** rechtstreeks equivalent, en waarom?

### Vraag 13 [Analyse]

Het team stelt voor om de productie uit te rollen met `podman compose -f compose.yaml -f compose.prod.yaml up -d` op één enkele VM. In welke gevallen is dat een redelijke beslissing? Noem vier dingen die deze oplossing niet biedt, en het signaal dat aangeeft dat het tijd is voor een orchestrator.
