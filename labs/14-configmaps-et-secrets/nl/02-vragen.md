# Lab 14 — Vragen

---

### Vraag 1 [Begrip]

Koppel elk mechanisme van lab 08 aan zijn Kubernetes-equivalent: `ENV` in de Dockerfile, `-e`, `--env-file api.env`, een `application.yaml` gemount als bind mount, `podman secret` + `_FILE`. Welk heeft **geen** equivalent in een manifest, en waarom is dat een goede zaak?

### Vraag 2 [Voorspelling]

```bash
kubectl patch configmap api-config -p '{"data":{"APP_MESSAGE":"message modifie"}}'
kubectl exec deploy/api -- env | grep APP_MESSAGE
kubectl patch configmap web-html -p '{"data":{"index.html":"<h1>modifie</h1>"}}'
sleep 60 ; kubectl exec deploy/web -- cat /usr/share/nginx/html/index.html
```

De API krijgt `api-config` via `envFrom`, de frontend mount `web-html` als volume. Voorspel de twee uitvoeren en verklaar het verschil in gedrag. Wat moet er gebeuren opdat de API het nieuwe bericht ziet?

### Vraag 3 [Diagnose]

```bash
$ kubectl get pods
NAME                   READY   STATUS                       RESTARTS   AGE
api-5dff955d5b-rz7sd   0/1     CreateContainerConfigError   0          8s
api-d7c644f6c-fpwxr    1/1     Running                      0          61s
```

Er is net een rollout gestart na het toevoegen van een variabele `valueFrom: configMapKeyRef`. Geef het commando dat de oorzaak onthult, de verwachte boodschap, en leg uit waarom de oude Pod nog draait.

### Vraag 4 [Analyse]

Een collega beweert dat Secrets "versleuteld zijn, dus veilig". Toon hem in één commando wat die versleuteling waard is, som dan op wat een Secret **werkelijk** toevoegt ten opzichte van een ConfigMap, en de drie maatregelen die een Secret veilig maken in een bedrijfscluster.

### Vraag 5 [Analyse]

Voor het wachtwoord van de database zijn twee inspuitingen mogelijk in het template van de API: `env: [{name: DB_PASSWORD, valueFrom: {secretKeyRef: …}}]` of een volume `secret:` gemount onder `/run/secrets/db` met `DB_PASSWORD_FILE`. Vergelijk ze op drie criteria: zichtbaarheid in `kubectl exec … env`, bijwerking na rotatie van het Secret, en compatibiliteit met Spring Boot. Welke kiest men?

### Vraag 6 [Diagnose]

Een ontwikkelaar mount een ConfigMap met `subPath: default.conf` om maar één bestand in `/etc/nginx/conf.d/` te vervangen zonder de andere te verbergen. Daarna wijzigt hij de ConfigMap en wacht: er verandert niets, zelfs niet na tien minuten. Leg uit waarom, en geef twee manieren om eruit te komen.

### Vraag 7 [Voorspelling]

Het Deployment `api` verwijst naar `api-config` en `db-secret`. Je past **precies** hetzelfde Deployment-bestand toe in de namespace `prod`, waar een ConfigMap `api-config` (`APP_PROFILE: prod`) en een Secret `db-secret` (een ander wachtwoord) bestaan. Wat gebeurt er, en wat toont dat aan over het promoveren van een image?

### Vraag 8 [Begrip]

Leg uit wat `kubectl create secret generic db --from-literal=password=x --dry-run=client -o yaml` produceert, waarom je het gebruikt in plaats van de YAML met de hand te schrijven, en wat je met het resultaat **niet** mag doen.

### Vraag 9 [Analyse]

Een `kubectl get secret db-secret -o yaml` is in een ticket geplakt om "de config te tonen". Pas de procedure van lab 08 (vraag 13) toe op dit geval: welke stappen, en wat maakt, in de manier waarop het Secret in de Pods ingespoten wordt, de rotatie snel of traag?

### Vraag 10 [Diagnose]

De Pod `web` start maar nginx geeft `403 Forbidden` op `/`. `kubectl exec deploy/web -- ls -l /usr/share/nginx/html/` toont een **lege** map. De ConfigMap `web-html` bestaat, met een sleutel `index.html`. Wat is waarschijnlijk vergeten in het template, en hoe ga je dat na met `kubectl get pod -o yaml`?

### Vraag 11 [Analyse]

Waarom mount het lab de ConfigMap `web-nginx` op de hele map `/etc/nginx/conf.d`, terwijl de image `nginx:alpine` daar al een `default.conf` bevat? Wat gebeurt er met dat oorspronkelijke bestand, en wat zou je moeten doen om een tweede `.conf`-bestand toe te voegen zonder alles te verbergen?

### Vraag 12 [Analyse]

Vergelijk `immutable: true` op een ConfigMap met het versioneren van haar naam (`api-config-v2`) en het wijzigen van de verwijzing in het Deployment. Wat win je in elk geval, en waarom genereren Kustomize en Helm namen met een hash-achtervoegsel?

### Vraag 13 [Analyse]

Het platformteam legt op: "geen enkel Secret in Git". Beschrijf hoe, met een External Secrets Operator (of Sealed Secrets), de repository toch alles kan bevatten wat nodig is om de applicatie uit te rollen, wat de repository precies bevat, en wat het Secret in het cluster aanmaakt. Wat is het verband met de secretsbeheerder van lab 08?
