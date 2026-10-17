# Lab 14 — Questions

---

### Question 1 [Understanding]

Match each lab 08 mechanism to its Kubernetes equivalent: `ENV` in the Dockerfile, `-e`, `--env-file api.env`, an `application.yaml` bind-mounted, `podman secret` + `_FILE`. Which one has **no** equivalent in a manifest, and why is that a good thing?

### Question 2 [Prediction]

```bash
kubectl patch configmap api-config -p '{"data":{"APP_MESSAGE":"message modifie"}}'
kubectl exec deploy/api -- env | grep APP_MESSAGE
kubectl patch configmap web-html -p '{"data":{"index.html":"<h1>modifie</h1>"}}'
sleep 60 ; kubectl exec deploy/web -- cat /usr/share/nginx/html/index.html
```

The API receives `api-config` through `envFrom`, the front end mounts `web-html` as a volume. Predict the two outputs and explain the difference in behaviour. What must be done for the API to see the new message?

### Question 3 [Diagnosis]

```bash
$ kubectl get pods
NAME                   READY   STATUS                       RESTARTS   AGE
api-5dff955d5b-rz7sd   0/1     CreateContainerConfigError   0          8s
api-d7c644f6c-fpwxr    1/1     Running                      0          61s
```

A rollout has just been launched after adding a `valueFrom: configMapKeyRef` variable. Give the command that reveals the cause, the expected message, and explain why the old Pod is still running.

### Question 4 [Analysis]

A colleague claims that Secrets are "encrypted, therefore safe". Show them in one command what that encryption is worth, then list what a Secret **really** brings compared with a ConfigMap, and the three measures that make a Secret safe in an enterprise cluster.

### Question 5 [Analysis]

For the database password, two injections are possible in the API template: `env: [{name: DB_PASSWORD, valueFrom: {secretKeyRef: …}}]` or a `secret:` volume mounted under `/run/secrets/db` with `DB_PASSWORD_FILE`. Compare them on three criteria: visibility in `kubectl exec … env`, update after a Secret rotation, and compatibility with Spring Boot. Which one is chosen?

### Question 6 [Diagnosis]

A developer mounts a ConfigMap with `subPath: default.conf` to replace only one file in `/etc/nginx/conf.d/` without hiding the others. They then modify the ConfigMap and wait: nothing changes, even after ten minutes. Explain why, and give two ways out.

### Question 7 [Prediction]

The `api` Deployment references `api-config` and `db-secret`. You apply **exactly** the same Deployment file in the `prod` namespace, where an `api-config` ConfigMap (`APP_PROFILE: prod`) and a `db-secret` Secret (another password) exist. What happens, and what does that demonstrate about promoting an image?

### Question 8 [Understanding]

Explain what `kubectl create secret generic db --from-literal=password=x --dry-run=client -o yaml` produces, why it is used rather than writing the YAML by hand, and what must **not** be done with the result.

### Question 9 [Analysis]

A `kubectl get secret db-secret -o yaml` was pasted into a ticket to "show the config". Apply the lab 08 procedure (question 13) to this case: which steps, and what, in the way the Secret is injected into the Pods, makes the rotation fast or slow?

### Question 10 [Diagnosis]

The `web` Pod starts but nginx returns `403 Forbidden` on `/`. `kubectl exec deploy/web -- ls -l /usr/share/nginx/html/` shows an **empty** directory. The `web-html` ConfigMap exists, with an `index.html` key. What was probably forgotten in the template, and how do you check it with `kubectl get pod -o yaml`?

### Question 11 [Analysis]

Why does the lab mount the `web-nginx` ConfigMap on the whole `/etc/nginx/conf.d` directory, when the `nginx:alpine` image already contains a `default.conf` there? What becomes of that original file, and what would be needed to add a second `.conf` file without hiding everything?

### Question 12 [Analysis]

Compare `immutable: true` on a ConfigMap with versioning its name (`api-config-v2`) and changing the reference in the Deployment. What is gained in each case, and why do Kustomize and Helm generate names with a hash suffix?

### Question 13 [Analysis]

The platform team mandates: "no Secret in Git". Describe how, with an External Secrets Operator (or Sealed Secrets), the repository can still hold everything needed to deploy the application, what exactly the repository contains, and what creates the Secret in the cluster. What is the link with the secrets manager of lab 08?
