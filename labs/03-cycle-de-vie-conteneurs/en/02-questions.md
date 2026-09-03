# Lab 03 — Questions

---

### Question 1 [Understanding]

`podman run alpine` returns immediately, `podman run nginx` blocks the terminal, and `podman run -it alpine sh` opens a shell. Explain all three behaviours with **a single rule**.

### Question 2 [Diagnosis]

A developer containerises the in-house API and puts this start-up script into the image:

```sh
#!/bin/sh
java -jar /app/api.jar &
echo "API started"
```

The container prints "API started" and then exits immediately with code `0`. Explain precisely what happens, and fix the script.

### Question 3 [Analysis]

You run `podman run -d --name idle alpine sleep 300`, then `podman stop idle`. The command takes **10 seconds** to return, prints the warning `StopSignal SIGTERM failed to stop container idle in 10 seconds, resorting to SIGKILL`, and the container ends with code `137`. Yet `sleep` has nothing to save. Why did it not stop immediately, and why `137` rather than `143`?

### Question 4 [Analysis]

Repeat question 3, but with `podman run -d --init --name idle alpine sleep 300`. This time the `stop` returns **instantly** and the exit code is `143`. What exactly did `--init` change? What would `podman exec idle ps` show?

### Question 5 [Understanding]

Explain the difference between `-i` and `-t`. What happens, concretely, if you run `podman run -t alpine sh` (without `-i`) and then type `ls`? And with `podman run -i alpine sh` (without `-t`)?

### Question 6 [Diagnosis]

A colleague runs `podman attach my-api` to read the logs, presses `Ctrl+C` to leave… and production goes down. Explain what happened, and give the two correct ways to do what they originally wanted.

### Question 7 [Analysis]

After an incident, `podman ps -a` shows:

```
NAMES     STATUS
api       Exited (137) 4 minutes ago
worker    Exited (143) 4 minutes ago
batch     Exited (127) 4 minutes ago
```

For each of the three, say what most likely happened and which command you would run next to confirm it.

### Question 8 [Analysis]

Your Spring Boot application writes its logs to `/var/log/api/application.log` using `logging.file.name`, just like on the old servers. `podman logs api` returns nothing. Explain why — naming the process that captures logs in Podman — and explain why the "solution" of mounting that folder on the host is still a bad answer.

### Question 9 [Understanding]

`podman stop` followed by `podman start` on a PostgreSQL container: is the data preserved? And after `podman rm` followed by a fresh `podman run`? Explain the difference in terms of the underlying mechanism.

### Question 10 [Analysis]

An administrator who is used to Docker runs `podman run -d --restart=always --name api my-api:1.0` on a Podman server, checks that the container does restart when they kill it, then reboots the server for a kernel update. After the reboot, `podman ps` is empty. Explain why, and describe the Podman way to guarantee that a container starts at boot.

### Question 11 [Diagnosis]

A container with `--restart=on-failure:5` restarted five times and then stopped for good. Where do you find the logs of the **first** attempt, the one containing the root cause? And what happens if you run `podman restart` before looking?

### Question 12 [Analysis]

A container is eating 100% of one core and no longer responds. You want to know what it is doing before you kill it. Rank these commands from least to most intrusive, and say what each one tells you: `podman logs`, `podman top`, `podman stats`, `podman exec`, `podman inspect`.

### Question 13 [Understanding]

Why don't we put the Spring Boot API and its PostgreSQL database in the same container, even though that would be simpler to start? Give three concrete consequences, based on what you know about the life cycle.

### Question 14 [Analysis]

`podman run --rm` is recommended for one-off commands but **discouraged** for a production service — and Podman actually refuses to combine it with `--restart`. Explain the reasoning in both cases: what exactly do you lose when a production container disappears on exit, and why is the combination contradictory?
