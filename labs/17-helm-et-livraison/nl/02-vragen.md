# Labo 17 — Vragen

---

### Vraag 1 [Begrip]

Leg het verschil uit tussen een chart, een release en een revision. Waar bewaart Helm 3/4 de geschiedenis van een release, en waarom maakt dat `helm rollback` mogelijk zonder enige servercomponent?

### Vraag 2 [Voorspelling]

```bash
helm install stack ./stack -n lab17 --create-namespace
helm upgrade stack ./stack --set api.replicas=3
helm upgrade stack ./stack --set api.message="v2"
helm get values stack
```

Wat toont het laatste commando? Hoeveel replica's van de API draaien er na het derde commando, en waarom? Wat zou je moeten veranderen om zowel drie replica's als de boodschap "v2" te krijgen?

### Vraag 3 [Diagnose]

```bash
$ helm list -A
Error: kubernetes cluster unreachable: Get "http://localhost:8080/version": dial tcp [::1]:8080: connect: connection refused
$ kubectl get nodes
NAME         STATUS   ROLES           AGE   VERSION
wsl-ubuntu   Ready    control-plane   6d    v1.34.1+k3s1
```

De cluster draait, `kubectl` ziet hem, `helm` niet. Leg uit, geef de correctie, en zeg waarom `kubectl` dat probleem niet heeft.

### Vraag 4 [Analyse]

De chart annoteert het Pod-template met `checksum/config: {{ include (print $.Template.BasePath "/configmap.yaml") . | sha256sum }}`. Leg uit wat dat teweegbrengt bij `helm upgrade --set api.message=anders`, wat er zonder die annotatie zou gebeuren (labo 14), en een geval waarin dit idioom een ongewenste herdeployment uitlokt.

### Vraag 5 [Voorspelling]

```bash
helm history stack          # revisions 1, 2, 3 ; 3 = deployed
helm rollback stack 1
helm history stack
helm uninstall stack
kubectl get pvc -n lab17
```

Beschrijf de geschiedenis na de rollback (aantal revisions, beschrijving van de laatste), en daarna wat `kubectl get pvc` toont. Waarom gedraagt Helm zich zo met PVC's, en welke handeling verwijdert de data echt?

### Vraag 6 [Analyse]

Vergelijk Helm en Kustomize: model, verspreiding, geschiedenis, gebruik. Een team moet (a) PostgreSQL en Prometheus van derden installeren, (b) zijn vier microservices in drie omgevingen deployen via Argo CD. Wat zou je kiezen voor elke behoefte, en waarom leven de twee vaak samen?

### Vraag 7 [Diagnose]

```yaml
# overlays/prod/kustomization.yaml
resources: [../../base]
images:
  - name: localhost/api
    newTag: "1.1"
labels:
  - pairs: { env: prod }
    includeSelectors: false
```

Na `kubectl apply -k overlays/prod` dragen de Pods van de API wel de image 1.1, maar **niet** het label `env=prod`; het Deployment wel. Leg uit, corrigeer, en zeg waarom `includeSelectors: true` op een bestaand Deployment een slecht idee zou zijn.

### Vraag 8 [Analyse]

`podman image inspect api:1.1 --format '{{.Digest}}'` toont `sha256:e1b2…`; `podman push --digestfile` schrijft `sha256:b820…`; `kubectl get pod -o jsonpath='{..imageID}'` toont `localhost:5000/api@sha256:b820…`. Leg uit waarom twee verschillende digests dezelfde image aanduiden, welke je in productie moet vastpinnen, en waarom een tag niet volstaat.

### Vraag 9 [Diagnose]

Een Pod blijft in `ImagePullBackOff` met `failed to pull image "registry.intern:5000/api:1.1": … http: server gave HTTP response to HTTPS client`. Dezelfde registry werkt wel als `localhost:5000`. Leg het verschil in behandeling uit, geef het bestand en de inhoud die je op k3s schrijft, en wat je daarna moet doen. Wat doe je op een beheerde cluster waar je geen toegang hebt tot de nodes?

### Vraag 10 [Analyse]

Een pipeline voert `helm upgrade --install api ./chart --set api.image.tag=$CI_COMMIT_SHA --wait --timeout 5m` uit met een kubeconfig. Zeg wat `--install`, `--wait` en `--timeout` bijbrengen, welke kubeconfig de runner zou moeten hebben (labo 16), en wat hij moet doen als het commando faalt.

### Vraag 11 [Begrip]

Leg GitOps uit door "de CI pusht naar de cluster" tegenover "de cluster pullt uit Git" te zetten. Welke concrete voordelen (audit, rollback, afwijking) en welk gevolg voor wat de CI nog mag doen? Leg het verband met de reconciliatielus van labo 11.

### Vraag 12 [Analyse]

Je chart werkt op k3s met `Service: LoadBalancer`, `local-path` en de Traefik-Ingress. Som op wat er concreet verandert bij de overstap naar EKS/AKS/GKE, en daarna naar OpenShift, en wat niet verandert. Hoe schrijf je de chart zodat ze overdraagbaar blijft?

### Vraag 13 [Analyse]

Een ontwikkelaar stelt voor: "we zetten overal `latest`, `imagePullPolicy: Always`, en de CI doet `kubectl rollout restart` na elke push: geen tags of charts meer te veranderen". Ontkracht het voorstel punt per punt (reproduceerbaarheid, rollback, audit, beveiliging), en stel daarna de juiste versie voor met de tools van dit labo.
