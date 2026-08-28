# Lab 02 — Hands-on lab: dissect an image, run a registry

*Goal: handle tags, layers and digests, then publish an image to a private registry you run yourself — and discover on the way why Podman makes you write names in full.*

**Prerequisites** — Lab 01 done (rootless Podman under WSL, `systemd` active). Port `5000` must be free (`ss -lntp | grep :5000` must return nothing).

**Files provided** — `files/Dockerfile` (two lines, explained in lab 04; here it only serves as an image generator).

---

## Step 1 — Read an image name

```bash
podman pull nginx:alpine
podman pull alpine
```

**Observe** `Resolved "nginx" as an alias`, then `Trying to pull docker.io/library/nginx:alpine...`, the `Copying blob` lines, and for `alpine` a bare identifier: the image has been there since lab 01.

```bash
podman image inspect --format '{{.RepoTags}}'  nginx:alpine
podman image inspect --format '{{.Digest}}'    nginx:alpine
```

**Observe** on one side `[docker.io/library/nginx:alpine]` — the **full** name, which you did not type — on the other `sha256:1f25fedd50aec27413031afb…`.

*Explanation.* `nginx:alpine` is a readable, movable name; the digest is the real, permanent identity of the content. Podman always shows the full name: there is no "short name" in its storage, only in your command.

Now try a name that is not in the alias list:

```bash
grep -c '=' /etc/containers/registries.conf.d/000-shortnames.conf
grep -E '^\s*"(alpine|nginx|eclipse-temurin)"' /etc/containers/registries.conf.d/000-shortnames.conf
grep unqualified-search-registries /etc/containers/registries.conf
```

**Observe** that `alpine` and `nginx` have an alias, `eclipse-temurin` does not, and that Ubuntu's search list only contains `docker.io` — which is why `podman pull eclipse-temurin:21-jre-alpine` works anyway for you, whereas it would ask a question on Fedora.

> **Podman** — A short name is a terminal convenience, not a company practice. In a Dockerfile or a script, write `docker.io/library/eclipse-temurin:21-jre-alpine`: the result will no longer depend on the configuration of the machine that runs it.

---

## Step 2 — List your images

```bash
podman images
```

**Observe** the `REPOSITORY / TAG / IMAGE ID / CREATED / SIZE` columns, and repositories written in full: `docker.io/library/nginx`, `docker.io/library/alpine`.

```bash
podman images --format 'table {{.Repository}}\t{{.Tag}}\t{{.Size}}'
podman images --format '{{.Repository}}:{{.Tag}}'
```

*Explanation.* Get used to `--format`: it makes your commands independent of presentation changes, and usable in scripts.

---

## Step 3 — The layers, and where the weight goes

```bash
podman history nginx:alpine --format 'table {{.Size}}\t{{.CreatedBy}}'
```

**Observe** a single big layer (`50.7MB`, the nginx installation), a few small `COPY` layers of scripts, an `8.7MB` layer (Alpine) at the very bottom, and many `0B` lines.

*Explanation.* The `0B` lines are **metadata** instructions: `ENV`, `CMD`, `EXPOSE`, `ENTRYPOINT`, `STOPSIGNAL`. They create no file. This command is your first reflex when an image is abnormally heavy: the guilty line jumps out.

Podman can also show the layers as a tree, with their source image:

```bash
podman image tree nginx:alpine
```

**Observe** the first layer marked `Top Layer of: [docker.io/library/alpine:latest]`: nginx:alpine is **built on** the alpine image you already have — that 8.7 MB layer is stored only once.

```bash
podman system df
podman system df -v | head -n 12
```

**Observe** in verbose mode the `SHARED SIZE` column: `8.698MB` for `nginx` and for `alpine`, the same layer counted in both.

---

## Step 4 — `podman tag` copies nothing

```bash
podman tag nginx:alpine my-nginx:v1
podman tag nginx:alpine my-nginx:preprod
podman images --format 'table {{.Repository}}\t{{.Tag}}\t{{.ID}}' | grep nginx
```

**Observe** three lines… with **the same `IMAGE ID`** — and your two new names prefixed with `localhost/`.

```bash
podman rmi my-nginx:v1
```

**Observe** the output: only `Untagged: localhost/my-nginx:v1`. No `Deleted:`.

```bash
podman rmi my-nginx:preprod
```

**Observe** again `Untagged:` only — because `docker.io/library/nginx:alpine` still designates the image.

*Explanation.* A tag is a reference. As long as a name remains, the data remains. That is why "I did some `rmi` and got no space back" is a frequent and perfectly normal complaint. As for `localhost/`: an image you name without a registry belongs to no registry, and Podman says so.

---

## Step 5 — Build two versions of the same image

Copy the provided file into a working folder:

```bash
mkdir -p ~/labo-docker/02 && cd ~/labo-docker/02
cp <lab-path>/files/Dockerfile .
cat Dockerfile
```

```bash
podman build -t demo-layers:1.0 .
podman history demo-layers:1.0 --format 'table {{.ID}}\t{{.Size}}\t{{.CreatedBy}}'
```

**Observe** the lines `STEP 1/2`, `STEP 2/2`, `COMMIT demo-layers:1.0`, `Successfully tagged localhost/demo-layers:1.0`, then three layers: your `RUN` (`2.05kB`), the base image's `CMD` (`0B`), and the Alpine file system (`8.7MB`), marked `<missing>` because that layer belongs to another image.

Change the version then rebuild on **the same tag**:

```bash
sed -i 's/version 1/version 2/' Dockerfile
podman build -t demo-layers:1.0 .
podman run --rm demo-layers:1.0 cat /version.txt
```

**Observe** `version 2`, and a new `IMAGE ID` for the same tag.

```bash
podman images --filter dangling=true
```

**Observe** a `<none> <none>` line with the **old** `IMAGE ID`: that is the *dangling* image, the one that lost its name. It still takes 8.7 MB (shared, as it happens).

*Explanation.* The tag `demo-layers:1.0` was **moved** to a new image: exactly the scenario of question 2. Nothing warns the user. Remove the residue by its identifier:

```bash
podman rmi $(podman images --filter dangling=true -q)
```

---

## Step 6 — Run a private registry

A registry is nothing but a container:

```bash
podman run -d -p 5000:5000 --name lab-registry registry:2
podman ps --filter name=lab-registry
curl -s http://localhost:5000/v2/_catalog
```

**Observe** `0.0.0.0:5000->5000/tcp` in the `PORTS` column, then `{"repositories":[]}`: the registry is empty and working.

> **Windows / WSL** — That port 5000 is published inside the WSL VM, but Windows sees it too: open `http://localhost:5000/v2/_catalog` in your Windows browser. WSL 2 automatically relays ports listened on in Linux to `localhost` on the Windows side (*localhost forwarding*). That is what will let you test the Angular front end from Edge or Chrome in later labs.

Publish your image to it:

```bash
podman tag demo-layers:1.0 localhost:5000/base/demo:1.0
podman push localhost:5000/base/demo:1.0
```

**Observe** the failure:

```
Error: … pinging container registry localhost:5000: Get "https://localhost:5000/v2/":
http: server gave HTTP response to HTTPS client
```

*Explanation.* Your registry speaks HTTP; Podman requires HTTPS by default, **even for localhost** — where Docker makes a silent exception. For a test registry, you say so explicitly:

```bash
podman push --tls-verify=false localhost:5000/base/demo:1.0
curl -s http://localhost:5000/v2/_catalog
curl -s http://localhost:5000/v2/base/demo/tags/list
```

**Observe** the `Copying blob` lines, `Writing manifest to image destination`, then `{"repositories":["base/demo"]}` and `{"name":"base/demo","tags":["1.0"]}`.

> **Security** — The alternative is to declare the registry in `~/.config/containers/registries.conf` (`[[registry]]`, `location = "localhost:5000"`, `insecure = true`). It is convenient on a development workstation, and dangerous everywhere else: an "insecure" registry is one whose identity and encryption are not verified, so one in which an attacker on the network can substitute an image. In a company, a registry has a certificate, full stop.

You have just reproduced, in three commands, what your company's CI does. Check the differential transfer:

```bash
podman tag demo-layers:1.0 localhost:5000/base/demo:1.1
podman push --tls-verify=false localhost:5000/base/demo:1.1
```

**Observe** that the same blobs are named but the transfer is instantaneous: the registry already has them, only the manifest is written.

---

## Step 7 — Pull by digest

Get the digest as the registry knows it:

```bash
curl -sI -H "Accept: application/vnd.oci.image.manifest.v1+json" \
  http://localhost:5000/v2/base/demo/manifests/1.0 | grep -i docker-content-digest
```

**Observe** a line `Docker-Content-Digest: sha256:239accdd…`. Copy that value.

```bash
podman rmi localhost:5000/base/demo:1.0
podman pull --tls-verify=false localhost:5000/base/demo@sha256:<paste_here>
podman images --format 'table {{.Repository}}\t{{.Tag}}\t{{.ID}}\t{{.Digest}}' | grep demo
```

**Observe** that the image is pulled and that `podman image inspect --format '{{.Digest}}' demo-layers:1.0` gives exactly the value you just pasted.

*Explanation.* This is the form used by serious deployments: it is **tamper-proof**. Even if someone republishes `base/demo:1.0` with different content, your digest keeps designating the image you tested.

---

## Step 8 — Carry an image without a network

```bash
podman save -o /tmp/demo.tar demo-layers:1.0
ls -lh /tmp/demo.tar
tar -tf /tmp/demo.tar | head -n 4
```

**Observe** an `8.4M` archive containing `<sha256>.tar` files (the layers), a `.json` (the configuration) and a `manifest.json`: this is the historical `docker-archive` format.

```bash
podman save --format oci-archive -o /tmp/demo-oci.tar demo-layers:1.0
tar -tf /tmp/demo-oci.tar | head -n 4
```

**Observe** this time `blobs/sha256/…` and `index.json`: the **OCI** layout, the one every tool (Docker, Podman, skopeo, Kubernetes) reads.

Compare with `export`, which works on a **container**:

```bash
podman run -d --name tmpx nginx:alpine
podman export tmpx | podman import - nginx-flat:v1
podman image inspect --format '{{json .Config.Cmd}}' nginx-flat:v1
podman run --rm nginx-flat:v1
```

**Observe** `null`, then the error `crun: cannot find `` in $PATH`: the imported image **no longer knows what to launch**.

*Explanation.* Remember the rule: `save`/`load` for an image, `export`/`import` never for deployment.

```bash
podman rmi demo-layers:1.0 localhost:5000/base/demo:1.1
podman load -i /tmp/demo.tar
```

**Observe** `Loaded image: localhost/demo-layers:1.0`: the tag came back with the archive.

---

## Clean-up

```bash
podman rm -f -t 0 tmpx lab-registry
podman rmi nginx-flat:v1 demo-layers:1.0 registry:2
podman images --format '{{.Repository}}:{{.Tag}}' | grep -E 'demo|flat|registry'
rm -f /tmp/demo.tar /tmp/demo-oci.tar
```

The image pulled by digest in step 7 may remain:

```bash
podman images --format 'table {{.ID}}\t{{.Repository}}' | grep localhost:5000
podman rmi <ID>
```

**Observe** that only `docker.io/library/alpine` and `docker.io/library/nginx:alpine` remain, kept for what follows.

---

## What you must be able to state now

- A tag is a movable reference; the digest identifies content. Podman stores and shows full names, and prefixes yours with `localhost/`.
- `podman history` and `podman image tree` reveal where an image's weight goes and what it shares.
- `podman tag` duplicates nothing; `podman rmi` first removes a name.
- A `push` only transfers the layers missing from the registry.
- A registry is a plain HTTP service, started with one command — but Podman requires TLS, unless `--tls-verify=false` is explicit.
- `export`/`import` destroys the image configuration; `save`/`load` preserves it, in `docker-archive` or `oci-archive` format.
