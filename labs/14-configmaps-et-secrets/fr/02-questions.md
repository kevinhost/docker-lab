# Labo 14 — Questions

---

### Question 1 [Compréhension]

Reliez chaque mécanisme du labo 08 à son équivalent Kubernetes : `ENV` dans le Dockerfile, `-e`, `--env-file api.env`, un `application.yaml` monté en bind mount, `podman secret` + `_FILE`. Lequel n'a **pas** d'équivalent dans un manifeste, et pourquoi est-ce une bonne chose ?

### Question 2 [Prédiction]

```bash
kubectl patch configmap api-config -p '{"data":{"APP_MESSAGE":"message modifie"}}'
kubectl exec deploy/api -- env | grep APP_MESSAGE
kubectl patch configmap web-html -p '{"data":{"index.html":"<h1>modifie</h1>"}}'
sleep 60 ; kubectl exec deploy/web -- cat /usr/share/nginx/html/index.html
```

L'API reçoit `api-config` par `envFrom`, le front monte `web-html` en volume. Prédisez les deux sorties et expliquez la différence de comportement. Que faut-il faire pour que l'API voie le nouveau message ?

### Question 3 [Diagnostic]

```bash
$ kubectl get pods
NAME                   READY   STATUS                       RESTARTS   AGE
api-5dff955d5b-rz7sd   0/1     CreateContainerConfigError   0          8s
api-d7c644f6c-fpwxr    1/1     Running                      0          61s
```

Un rollout vient d'être lancé après l'ajout d'une variable `valueFrom: configMapKeyRef`. Donnez la commande qui révèle la cause, le message attendu, et expliquez pourquoi l'ancien Pod tourne toujours.

### Question 4 [Analyse]

Un collègue affirme que les Secrets sont « chiffrés, donc sûrs ». Montrez-lui en une commande ce que vaut ce chiffrement, puis listez ce qu'un Secret apporte **réellement** par rapport à une ConfigMap, et les trois mesures qui rendent un Secret sûr dans un cluster d'entreprise.

### Question 5 [Analyse]

Pour le mot de passe de la base, deux injections possibles dans le template de l'API : `env: [{name: DB_PASSWORD, valueFrom: {secretKeyRef: …}}]` ou un volume `secret:` monté sous `/run/secrets/db` avec `DB_PASSWORD_FILE`. Comparez-les sur trois critères : visibilité dans `kubectl exec … env`, mise à jour après rotation du Secret, et compatibilité avec Spring Boot. Laquelle choisit-on ?

### Question 6 [Diagnostic]

Un développeur monte une ConfigMap avec `subPath: default.conf` pour ne remplacer qu'un fichier dans `/etc/nginx/conf.d/` sans masquer les autres. Il modifie ensuite la ConfigMap et attend : rien ne change, même après dix minutes. Expliquez pourquoi, et donnez deux façons de s'en sortir.

### Question 7 [Prédiction]

Le Deployment `api` référence `api-config` et `db-secret`. Vous appliquez **exactement** le même fichier de Deployment dans le namespace `prod`, où existent une ConfigMap `api-config` (`APP_PROFILE: prod`) et un Secret `db-secret` (un autre mot de passe). Que se passe-t-il, et qu'est-ce que cela démontre sur la promotion d'une image ?

### Question 8 [Compréhension]

Expliquez ce que `kubectl create secret generic db --from-literal=password=x --dry-run=client -o yaml` produit, pourquoi on l'utilise plutôt que d'écrire le YAML à la main, et ce qu'il **ne faut pas** faire avec le résultat.

### Question 9 [Analyse]

Un `kubectl get secret db-secret -o yaml` a été collé dans un ticket pour « montrer la config ». Appliquez la procédure du labo 08 (question 13) à ce cas : quelles étapes, et qu'est-ce qui, dans la façon dont le Secret est injecté dans les Pods, rend la rotation rapide ou lente ?

### Question 10 [Diagnostic]

Le Pod `web` démarre mais nginx renvoie `403 Forbidden` sur `/`. `kubectl exec deploy/web -- ls -l /usr/share/nginx/html/` montre un répertoire **vide**. La ConfigMap `web-html` existe, avec une clé `index.html`. Qu'est-ce qui a probablement été oublié dans le template, et comment le vérifier avec `kubectl get pod -o yaml` ?

### Question 11 [Analyse]

Pourquoi le labo monte-t-il la ConfigMap `web-nginx` sur le répertoire `/etc/nginx/conf.d` entier, alors que l'image `nginx:alpine` y contient déjà un `default.conf` ? Que devient ce fichier d'origine, et que faudrait-il faire pour ajouter un second fichier `.conf` sans tout masquer ?

### Question 12 [Analyse]

Comparez `immutable: true` sur une ConfigMap avec le fait de versionner son nom (`api-config-v2`) et de changer la référence dans le Deployment. Que gagne-t-on dans chaque cas, et pourquoi Kustomize et Helm génèrent-ils des noms avec un suffixe de hachage ?

### Question 13 [Analyse]

L'équipe plateforme impose : « aucun Secret dans Git ». Décrivez comment, avec un External Secrets Operator (ou Sealed Secrets), le dépôt peut quand même contenir tout ce qu'il faut pour déployer l'application, ce que contient exactement le dépôt, et ce qui crée le Secret dans le cluster. Quel est le lien avec le gestionnaire de secrets du labo 08 ?
