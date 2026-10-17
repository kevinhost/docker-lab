#!/usr/bin/env bash
# Environnement de VERIFICATION de la partie Kubernetes : un k3s mono-noeud
# (image officielle rancher/k3s, meme version que celle recommandee a l'apprenant)
# qui tourne dans un conteneur Docker privilegie de cette machine.
#
#   tools/k3s-sandbox.sh up                    # cree/demarre le cluster, attend le noeud Ready
#   tools/k3s-sandbox.sh run 'kubectl get nodes'
#   tools/k3s-sandbox.sh shell                 # shell interactif dans le conteneur k3s
#   tools/k3s-sandbox.sh copy-labs             # recopie labs/ dans /root/labs
#   tools/k3s-sandbox.sh import-image api:1.0  # podman save (bac a sable Podman) -> ctr images import
#   tools/k3s-sandbox.sh replay script.sh      # rejoue un script WSL (sudo k3s ctr/crictl, curl traduits)
#   tools/k3s-sandbox.sh down                  # supprime le cluster
#
# Ce qui est reproduit : la meme version de k3s que sur WSL (Traefik, ServiceLB,
# local-path, metrics-server, CoreDNS), le nom de noeud "wsl-ubuntu", le kubeconfig
# en mode 644, l'import d'images construites avec Podman.
# Ce qui n'est PAS reproduit : systemd (pas de service k3s ; `wsl --shutdown` se
# simule par `docker restart`), le script get.k3s.io, le noyau WSL, le forwarding
# localhost vers Windows. Ces points sont decrits « tels que sur WSL » dans les labos.
set -euo pipefail

NAME=k3slab
PODMAN_NAME=podlab
IMAGE=docker.io/rancher/k3s:v1.34.1-k3s1
ROOT="$(cd "$(dirname "$0")/.." && pwd)"

up() {
  if docker ps -a --format '{{.Names}}' | grep -qx "$NAME"; then
    docker start "$NAME" >/dev/null
  else
    docker run -d --privileged --name "$NAME" --hostname wsl-ubuntu \
      -p 127.0.0.1:16443:6443 -p 127.0.0.1:30080:30080 -p 127.0.0.1:30443:80 \
      "$IMAGE" server --write-kubeconfig-mode 644 >/dev/null
  fi
  for i in $(seq 1 60); do
    if docker exec "$NAME" kubectl get nodes 2>/dev/null | grep -q ' Ready'; then
      docker exec "$NAME" mkdir -p /root   # l'image k3s n'a pas de /root
      echo "Cluster '$NAME' pret : $(docker exec "$NAME" k3s --version | head -1)"
      return 0
    fi
    sleep 3
  done
  echo "le noeud n'est pas Ready apres 180 s" >&2
  return 1
}

run() {
  docker exec -w /root "$NAME" sh -c "$1"
}

shell() {
  docker exec -it -w /root "$NAME" sh
}

copy_labs() {
  docker exec "$NAME" rm -rf /root/labs
  docker cp "$ROOT/labs" "$NAME":/root/labs
  echo "labs/ copie dans $NAME:/root/labs"
}

import_image() {
  # Reproduit `podman save IMAGE | sudo k3s ctr images import -` de l'apprenant,
  # entre le bac a sable Podman (podlab) et le cluster (k3slab).
  local img="${1:?image manquante (ex. localhost/api:1.0)}"
  # Dans l'image rancher/k3s, `k3s ctr` n'est pas disponible : on appelle ctr directement.
  docker exec -u podman -e HOME=/home/podman -e XDG_RUNTIME_DIR=/tmp/podman-run-1000 "$PODMAN_NAME" \
    podman save "$img" | docker exec -i "$NAME" ctr --address /run/k3s/containerd/containerd.sock -n k8s.io images import -
}

# Rejoue un script de labo ecrit pour WSL : `sudo k3s ctr` / `sudo k3s crictl` deviennent
# les appels directs du bac a sable, `curl` devient `wget -qO-` (BusyBox).
replay() {
  local script="${1:?script manquant}"
  sed -e 's#sudo k3s ctr#ctr --address /run/k3s/containerd/containerd.sock -n k8s.io#g' \
      -e 's#sudo k3s crictl#crictl --runtime-endpoint unix:///run/k3s/containerd/containerd.sock#g' \
      -e 's#\bcurl -s#wget -qO-#g' -e 's#<chemin-du-labo>#/root/labs/__LAB__#g' "$script" \
    | docker exec -i -w /root "$NAME" sh
}

case "${1:-}" in
  up) up ;;
  run) run "${2:?commande manquante}" ;;
  shell) shell ;;
  copy-labs) copy_labs ;;
  import-image) import_image "${2:-}" ;;
  replay) replay "${2:-}" ;;
  down) docker rm -f "$NAME" >/dev/null && echo "cluster '$NAME' supprime" ;;
  *) sed -n '2,20p' "$0"; exit 1 ;;
esac
