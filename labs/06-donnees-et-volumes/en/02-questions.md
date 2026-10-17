# Lab 06 — Questions

---

### Question 1 [Understanding]

A colleague claims: "I ran `podman stop db` and then `podman start db`, and my tables are still there. So container data persists just fine; no need for a volume." What did they observe correctly? In which everyday situations will their data still disappear?

### Question 2 [Diagnosis]

You run:

```bash
podman run -d --name web -p 18080:80 -v html:/usr/share/nginx/html:ro nginx:alpine
```

Your `html/` folder holds an `index.html` saying "Version 1", yet `curl localhost:18080` returns the default nginx welcome page. Explain precisely what happened, where that default page comes from, and fix the command.

### Question 3 [Diagnosis]

```bash
$ ls ~/.local/share/containers/storage/volumes/pgdata/_data
ls: cannot open directory '…/pgdata/_data': Permission denied
```

"But I am root inside the container, and this is my own home directory!" Explain why this refusal is normal, who owns those files as seen from the host, and give the command that lists them.

### Question 4 [Prediction]

```bash
podman run -d --name db -e POSTGRES_PASSWORD=alpha -v pgdata:/var/lib/postgresql/data postgres:16-alpine
podman rm -f -t 0 db
podman run -d --name db -e POSTGRES_PASSWORD=bravo -v pgdata:/var/lib/postgresql/data postgres:16-alpine
```

Which password lets you connect to the second container: `alpha`, `bravo`, both? Why?

### Question 5 [Analysis]

For each of the following needs, choose between named volume, bind mount and tmpfs, and justify in one sentence: (a) the sources of an Angular front end during development; (b) PostgreSQL's files; (c) the `nginx.conf` of a reverse proxy; (d) the intermediate files of a PDF conversion that can reach 2 GB.

### Question 6 [Diagnosis]

```bash
$ mkdir output
$ podman run --rm --user 1000 -v ./output:/out alpine sh -c 'id -u; echo x > /out/f'
1000
sh: can't create /out/f: Permission denied
$ ls -ln output
total 0        ← the folder belongs to 1000:1000
```

User 1000 cannot write into a folder owned by UID 1000. Explain the paradox and propose two different fixes.

### Question 7 [Prediction]

You rerun the command from question 6 with `-v ./output:/out:U`. It succeeds. What does `ls -ln output` on the host now show as the owner of the folder and of the file? How do you give the folder back to your own user?

### Question 8 [Analysis]

On a test server, `podman volume ls` shows fourteen volumes whose names are 64-character hashes. Where do they come from? For each one, how do you find out whether it is still in use, and by what? How do you stop the list from growing? And why is `podman volume prune` not the right reflex?

### Question 9 [Understanding]

A colleague backs up the production database every night with `tar czf backup.tgz` on the volume's directory, while PostgreSQL is running. The backups exist; nobody has ever tested a restore. What exactly is the risk? What are the two correct ways to do it, and which one do you pick for a daily backup?

### Question 10 [Analysis]

Compare `podman volume export pgdata -o pgdata.tar` with

```bash
podman run --rm -v pgdata:/data:ro -v ./:/backup alpine tar czf /backup/pgdata.tgz -C /data .
```

What exactly does the second command do, and why does it need a container to archive a directory that sits on your own disk? Which of the two also works with Docker?

### Question 11 [Analysis]

Why is it recommended to put a decrypted secret (private key, token) in a tmpfs rather than in the container's writable layer, when both disappear once the container is removed? What price does a tmpfs pay in memory?

### Question 12 [Diagnosis]

The command `podman run --rm -v ./conf:/etc/app:ro alpine cat /etc/app/app.yaml` works on your WSL. On one of the company's RHEL 9 servers, with the same file and the same permissions, it fails: `cat: can't open '/etc/app/app.yaml': Permission denied`. Even with `--user 0`. Diagnose, fix, and explain why the fix is harmless on Ubuntu.

### Question 13 [Analysis]

The team wants to run **two** containers of the Spring Boot API behind a load balancer, and plans to store user-uploaded documents in a named volume `uploads` mounted on `/app/uploads`. What is going to go wrong? Which solution do companies adopt, and how does it relate to the principle "a container is disposable"?
