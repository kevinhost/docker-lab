# Labo 13 — Questions

---

### Question 1 [Diagnostic]

```bash
$ kubectl get pods
NAME                   READY   STATUS             RESTARTS     AGE
api-6c7bb54fc5-2vs4k   1/1     Running            0            27s
web-5588bd85f8-j5nl5   0/1     CrashLoopBackOff   2 (6s ago)   27s
$ kubectl logs deploy/web --tail=1
nginx: [emerg] host not found in upstream "api" in /etc/nginx/conf.d/default.conf:15
```

L'API tourne. Pourquoi nginx ne trouve-t-il pas `api`, alors que la même configuration marchait au labo 07 avec un simple réseau Podman ? Que faut-il créer, et pourquoi `web` repart-il ensuite tout seul ?

### Question 2 [Compréhension]

Expliquez ce que sont, pour un Service `api`, l'**IP de cluster**, le **nom DNS** et les **EndpointSlices**, qui maintient chacun, et pourquoi `ping 10.43.3.7` ne répond jamais alors que `wget http://10.43.3.7:8080/` fonctionne.

### Question 3 [Prédiction]

Un Service `api` sélectionne `app: api` ; le Deployment passe de 2 à 3 réplicas, puis vous supprimez un Pod à la main, puis vous cassez la readiness d'un Pod. Que montre `kubectl get endpointslices` après chaque opération, et qu'a vu un client qui appelait `api:8080` pendant ce temps ?

### Question 4 [Diagnostic]

`kubectl get svc api` montre une ClusterIP et le port `8080/TCP`, mais `kubectl get endpointslices -l kubernetes.io/service-name=api` renvoie un slice **sans adresse**, et Traefik répond `503`. Les Pods sont `1/1 Running`. Citez les deux causes possibles, la commande qui les départage, et la correction de chacune.

### Question 5 [Analyse]

Comparez `ClusterIP`, `NodePort` et `LoadBalancer` pour exposer le front sur votre WSL : quelle URL dans chaque cas, ce que k3s fait de plus que Kubernetes nu pour le troisième, et pourquoi un second Service `LoadBalancer` sur le port 80 resterait `<pending>` chez k3s.

### Question 6 [Compréhension]

Depuis un Pod du namespace `lab13`, `wget http://api:8080/` fonctionne ; depuis un Pod du namespace `default`, il échoue. Expliquez avec le contenu de `/etc/resolv.conf` d'un Pod, et donnez le nom à utiliser depuis `default`.

### Question 7 [Analyse]

Un Service répartit les connexions, pas les requêtes. Expliquez la différence, ce que cela donne pour un client HTTP/1.1 avec *keep-alive* (ou une connexion JDBC) face à trois réplicas, et ce que l'Ingress change à ce comportement.

### Question 8 [Diagnostic]

```yaml
spec:
  selector:
    app: api
  ports:
    - port: 80
      targetPort: 8080
```

Avec ce Service, `wget http://api:8080/` échoue (`Connection refused`) mais `wget http://api/` fonctionne. Expliquez les deux ports, et dites ce que nginx doit écrire dans son `proxy_pass`.

### Question 9 [Analyse]

Décrivez le chemin d'une requête `GET /api/actuator/health` envoyée par un navigateur Windows à `http://localhost/` dans notre stack k3s : chaque composant traversé, dans l'ordre, et les deux reverse proxies impliqués. Comment simplifier la chaîne en déplaçant une règle ?

### Question 10 [Compréhension]

Quelle est la différence entre un objet `Ingress` et un *Ingress controller* ? Que se passe-t-il si l'on applique un Ingress dans un cluster sans controller ? Et pourquoi un `503 Service Unavailable` renvoyé par Traefik désigne-t-il presque toujours un problème d'endpoints et non de Traefik ?

### Question 11 [Diagnostic]

Une équipe déploie son application sur EKS avec les manifestes écrits sur k3s. Le Service `LoadBalancer` obtient bien une IP publique, mais l'Ingress reste sans `ADDRESS` et le site ne répond pas. Qu'est-ce qui manque, et pourquoi cela « marchait » sur k3s ?

### Question 12 [Analyse]

Le front appelle l'API par `/api/` (même origine) plutôt que par `http://api.example.com` (origine distincte). Rappelez pourquoi (labo 07), puis dites où ce routage `/api/` peut être fait dans notre stack — nginx ou Ingress — et les avantages de le confier à l'Ingress.

### Question 13 [Analyse]

Un développeur veut joindre la base PostgreSQL du cluster depuis DBeaver sur Windows. Trois options : `kubectl port-forward svc/db 5432:5432`, un NodePort, un LoadBalancer. Classez-les par exposition croissante, dites laquelle est acceptable en production et pourquoi, et quel objet manque encore pour que `db` ait un nom (indice : labo 15).
