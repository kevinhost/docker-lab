# Lab 07 — Questions

---

### Question 1 [Diagnosis]

The Spring Boot API starts in its container with `SPRING_DATASOURCE_URL=jdbc:postgresql://localhost:5432/app` and stops on `Connection refused`. Yet PostgreSQL runs in the `db` container, on the same user-defined network, and `podman exec db pg_isready` answers `accepting connections`. Explain, fix, and say what `localhost` designates inside each of the two containers.

### Question 2 [Understanding]

On an Ubuntu/WSL, `podman inspect --format '{{.NetworkSettings.IPAddress}}' api` prints an empty line, while `podman exec api ip -4 addr` does show an address — the very address of the WSL distribution. What is going on, and what would you change so that the container gets a `10.88.0.x` address?

### Question 3 [Prediction]

```bash
podman run -d --name a --network podman alpine sleep 1d
podman run -d --name b --network podman alpine sleep 1d
podman exec b ping -c1 10.88.0.2
podman exec b ping -c1 a
```

Predict the result of the two `ping` commands, then what changes if you replace `--network podman` with `--network stack` after a `podman network create stack`. Explain the difference through a field of `podman network inspect`.

### Question 4 [Analysis]

The API's Dockerfile contains `EXPOSE 8080`. A colleague runs `podman run -d --name api api:1.0`, then `curl localhost:8080/actuator/health` from WSL, and gets `Connection refused`. They add `-p 8080:8080`: it works. They conclude that `EXPOSE` "is useless". Are they right? What is `EXPOSE` for, and who reads it?

### Question 5 [Diagnosis]

```bash
$ podman run -d --name web -p 80:80 nginx:alpine
Error: rootlessport cannot expose privileged port 80, you can add 'net.ipv4.ip_unprivileged_port_start=80' to /etc/sysctl.conf (currently 1024), or choose a larger port number (>= 1024): listen tcp 0.0.0.0:80: bind: permission denied
```

Why does this error not appear with Docker (in classic mode)? Give three ways to serve the site on port 80 of the machine, and say which one you would choose in the workplace.

### Question 6 [Prediction]

`web` (nginx, `proxy_pass http://api:8080/`) and `api` run on the `stack` network; `curl localhost:18080/api/actuator/health` returns `200`. You run:

```bash
podman rm -f -t 0 api
podman run -d --name other --network stack alpine sleep 1d
podman run -d --name api --network stack api:1.0
```

What does the same `curl` return now, and why, when `podman run --rm --network stack alpine wget -qO- http://api:8080/actuator/health` works perfectly? How do you fix it?

### Question 7 [Analysis]

In nginx's logs, every request coming from your Windows browser shows, as the client address, the address of the `web` container itself (`10.89.0.10`). Explain where that address comes from, how this differs from root Docker, and what consequence it has for an application that logs or rate-limits by IP address.

### Question 8 [Understanding]

Can a container belong to two networks? Describe a concrete use case for the `web`/`api`/`db` stack, the commands required, and what `podman inspect api --format '{{json .NetworkSettings.Networks}}'` then shows.

### Question 9 [Diagnosis]

A colleague starts their API with `--network host` "to keep things simple". Name two things that work differently or not at all compared with a bridge network, and one case where `--network host` is legitimate. And what happens, under rootless, if the application listens on port 80?

### Question 10 [Analysis]

Compare a **network** `stack` holding `web` and `api` with a **pod** `stackpod` holding the same two containers: how does nginx refer to the API in each case, where is `-p` declared, and what does `podman ps --pod` show in addition? Why does this second model concern you even if you never use `podman pod`?

### Question 11 [Analysis]

During development, you want to connect DBeaver (on Windows) to the `db` database of the `stack` network, without the database being reachable by other machines on the company network. Give the exact `-p` option, say why the Windows browser reaches that port anyway despite `127.0.0.1`, and why you never do this in production.

### Question 12 [Diagnosis]

```bash
$ podman network rm stack
Error: "stack" has associated containers with it. Use -f to forcibly delete containers and pods: network is being used
```

What exactly does `-f` do, why is it a bad idea in a clean-up sequence, and what is the correct sequence?

### Question 13 [Analysis]

The front-end team calls the API directly from the browser at `http://localhost:8080` (the published port of `api`), and keeps fighting CORS errors. The ops team proposes publishing only `web` and having nginx relay `/api/`. Explain why that removes the CORS problem, what other benefits it brings, and which line of `nginx.conf` does the work.
