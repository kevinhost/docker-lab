# Lab 03 — Questions

---

### Question 1 [Understanding]

`podman run alpine` returns immediately, `podman run nginx` blocks the terminal, and `podman run -it alpine sh` opens a shell. Explain these three behaviours with **one and the same rule**.

### Question 2 [Diagnosis]

A developer containerises the in-house API and writes a start-up script into the image:

```sh
#!/bin/sh
java -jar /app/api.jar &
echo "API started"
```

The container does print "API started" then stops at once with code `0`. Explain precisely what happens, and fix the script.

### Question 3 [Analysis]

You run `podman run -d --name idle alpine sleep 300`, then `podman stop idle`. The command takes **10 seconds** to return, prints a warning `StopSignal SIGTERM failed to stop container idle in 10 seconds, resorting to SIGKILL`, and the container ends with code `137`. Yet `sleep` has nothing to save. Why did it not stop immediately, and why `137` rather than `143`?

### Question 4 [Analysis]

Take question 3 again, but with `podman run -d --init --name idle alpine sleep 300`. This time the `stop` returns **instantly** and the exit code is `143`. What exactly did `--init` change? What would you see in `podman exec idle ps`?

### Question 5 [Understanding]

Distinguish `-i` and `-t`. What concretely happens if you run `podman run -t alpine sh` (without `-i`) then type `ls`? And `podman run -i alpine sh` (without `-t`)?

### Question 6 [Diagnosis]

A colleague runs `podman attach my-api` to read the logs, presses `Ctrl+C` to leave… and production goes down. Explain what happened, and give the two correct ways to reach their original goal.

### Question 7 [Analysis]

After an incident, `podman ps -a` shows:

```
NAMES     STATUS
api       Exited (137) 4 minutes ago
worker    Exited (143) 4 minutes ago
batch     Exited (127) 4 minutes ago
```

For each of the three, say what most probably happened and which command you would run next to confirm it.

### Question 8 [Analysis]

Your Spring Boot application writes its logs to `/var/log/api/application.log` thanks to `logging.file.name`, as on the old servers. `podman logs api` returns nothing. Explain why — naming the process that captures logs in Podman — and say why the "solution" of mounting that folder on the host remains a bad answer.

### Question 9 [Understanding]

`podman stop` then `podman start` on a PostgreSQL container: is the data kept? And after `podman rm` then a new `podman run`? Explain the difference with the underlying mechanism.

### Question 10 [Analysis]

An administrator used to Docker runs `podman run -d --restart=always --name api my-api:1.0` on a Podman server, checks that the container does restart when they kill it, then reboots the server for a kernel update. On return, `podman ps` is empty. Explain why, and say what the Podman way is to guarantee a restart at boot.

### Question 11 [Diagnosis]

A container with `--restart=on-failure:5` restarted five times then stopped for good. Where do you find the logs of the **first** attempt, the one containing the root cause? What happens if you `podman restart` before having looked?

### Question 12 [Analysis]

A container is eating 100% of one core and no longer responds. You want to know what it is doing before killing it. Rank these commands from least to most intrusive, and say what each teaches you: `podman logs`, `podman top`, `podman stats`, `podman exec`, `podman inspect`.

### Question 13 [Understanding]

Why don't we put the Spring Boot API and its PostgreSQL database in the same container, even though it would be simpler to start? Give three concrete consequences, drawing on what you know of the life cycle.

### Question 14 [Analysis]

`podman run --rm` is recommended for one-off commands but **discouraged** for a production service — and Podman actually refuses to combine it with `--restart`. Explain the reasoning in both cases: what exactly is lost when a production container disappears on exit, and why is the combination contradictory?
