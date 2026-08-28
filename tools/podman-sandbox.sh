#!/usr/bin/env bash
# Environnement de VERIFICATION des labos : un Podman 5.x rootless, avec cgroups
# délégués, qui tourne dans un conteneur Docker privilégié de cette machine.
# Il sert à exécuter réellement chaque commande écrite dans un 04-labo-pratique.md
# quand Podman n'est pas installé sur la machine de rédaction.
#
#   tools/podman-sandbox.sh up            # crée/démarre le bac à sable
#   tools/podman-sandbox.sh run 'podman version'
#   tools/podman-sandbox.sh shell         # shell interactif rootless (user "podman")
#   tools/podman-sandbox.sh copy-labs     # recopie labs/ dans /home/podman/labs
#   tools/podman-sandbox.sh down          # supprime le bac à sable
#
# Le bac à sable reproduit une installation « apt install podman » sur Ubuntu/WSL :
#   - utilisateur non-root avec /etc/subuid et /etc/subgid
#   - unqualified-search-registries = ["docker.io"]
#   - cgroup v2 délégué (les limites --memory et `podman stats` fonctionnent)
# Ce qui n'est PAS reproduit : le noyau WSL (uname -r), systemd (cgroupManager
# vaut cgroupfs au lieu de systemd), Quadlet.
set -euo pipefail

NAME=podlab
IMAGE=quay.io/podman/stable
ROOT="$(cd "$(dirname "$0")/.." && pwd)"

up() {
  if docker ps -a --format '{{.Names}}' | grep -qx "$NAME"; then
    docker start "$NAME" >/dev/null
  else
    docker run -d --privileged --name "$NAME" --hostname wsl-ubuntu "$IMAGE" sleep infinity >/dev/null
  fi
  docker exec "$NAME" sh -c '
    set -e
    # Config "standard" (le conteneur podman/stable est livre avec une config imbriquee)
    cat > /etc/containers/containers.conf <<CONF
[containers]
log_driver = "k8s-file"
[engine]
cgroup_manager = "cgroupfs"
events_logger = "file"
runtime = "crun"
CONF
    rm -f /home/podman/.config/containers/containers.conf
    mkdir -p /home/podman/.config/containers
    printf "unqualified-search-registries = [\"docker.io\"]\n" > /home/podman/.config/containers/registries.conf
    chown -R podman:podman /home/podman/.config
    mkdir -p /tmp/podman-run-1000 && chown podman:podman /tmp/podman-run-1000 && chmod 700 /tmp/podman-run-1000
    # Delegation cgroup v2 : on vide la racine, on active les controleurs, on donne un sous-arbre a l utilisateur
    cd /sys/fs/cgroup
    mkdir -p init user
    for p in $(cat cgroup.procs); do echo $p > init/cgroup.procs 2>/dev/null || true; done
    echo "+memory +pids +cpu +cpuset +io" > cgroup.subtree_control
    chown -R podman:podman user
    sysctl -qw net.ipv4.ip_unprivileged_port_start=1024   # comme sur un vrai Linux : rootless => pas de port < 1024
    command -v ps >/dev/null || dnf -q -y install procps-ng iproute curl >/dev/null 2>&1 || true
  '
  echo "Bac a sable '$NAME' pret : $(run 'podman --version')"
}

run() {
  docker exec -u podman -w /home/podman -e HOME=/home/podman -e XDG_RUNTIME_DIR=/tmp/podman-run-1000 \
    "$NAME" bash -lc 'mkdir -p /sys/fs/cgroup/user/shell; echo $$ > /sys/fs/cgroup/user/shell/cgroup.procs;
      echo "+memory +pids +cpu +cpuset +io" > /sys/fs/cgroup/user/cgroup.subtree_control 2>/dev/null; '"$1"
}

shell() {
  docker exec -it -u podman -w /home/podman -e HOME=/home/podman -e XDG_RUNTIME_DIR=/tmp/podman-run-1000 \
    "$NAME" bash -lc 'mkdir -p /sys/fs/cgroup/user/shell; echo $$ > /sys/fs/cgroup/user/shell/cgroup.procs; exec bash'
}

copy_labs() {
  docker exec "$NAME" rm -rf /home/podman/labs
  docker cp "$ROOT/labs" "$NAME":/home/podman/labs
  docker exec "$NAME" chown -R podman:podman /home/podman/labs
  echo "labs/ copie dans $NAME:/home/podman/labs"
}

case "${1:-}" in
  up) up ;;
  run) run "${2:?commande manquante}" ;;
  shell) shell ;;
  copy-labs) copy_labs ;;
  down) docker rm -f "$NAME" >/dev/null && echo "Bac a sable supprime." ;;
  *) sed -n '2,20p' "$0"; exit 1 ;;
esac
