#!/bin/bash

# p2 Install script
# Installs and updates a p2 instance using k3s and docker
# Supported enviormnet variables:
# - STORAGE_BASE: Base directory in which p2 data will be storeed

K3S_VERSION="0.7.0"
P2_VERSION="0.7.4"
export INSTALL_K3S_EXEC="--docker --no-deploy traefik"

if [ "$EUID" -ne 0 ]; then
    echo "Please run as root"
    exit 1
fi

if ! [ -x "$(command -v curl)" ]; then
    echo 'Error: curl is not installed. Please make sure curl is installed and executable.' >&2
    exit 2
fi

# Create temporary folder and cd to it
TEMP_DIR=$(mktemp -d --suffix _p2)
cd "${TEMP_DIR}"

# kubectl helper functions, from https://github.com/zlabjp/kubernetes-scripts
function __is_pod_ready() {
  [[ "$(kubectl get po -n p2 "$1" -o 'jsonpath={.status.conditions[?(@.type=="Ready")].status}') 2>/dev/null" == 'True' ]]
}

function __pods_ready() {
  local pod

  [[ "$#" == 0 ]] && return 0

  for pod in $pods; do
    __is_pod_ready "$pod" || return 1
  done

  return 0
}

function __wait_until_pods_ready() {
  local i pods

  while true; do
    pods="$(kubectl get pods -n p2 -o 'jsonpath={.items[*].metadata.name}')"
    if __pods_ready $pods; then
      return 0
    fi

    echo " * Waiting for pods to be ready..."
    sleep 5
  done
}

# Make sure docker is installed
curl -fsSL https://get.docker.com -o install.docker.sh
bash install.docker.sh > /dev/null 2>&1
# Make sure K3s is installed
curl -fsSL "https://raw.githubusercontent.com/rancher/k3s/v${K3S_VERSION}/install.sh" -o install.k3s.sh
bash install.k3s.sh > /dev/null 2>&1

STORAGE_BASE="${STORAGE_BASE:-/srv/p2}"
P2_PASSWORD_FILE="${STORAGE_BASE}/password"

# Make sure storage directories exist
mkdir -p "${STORAGE_BASE}"

# Check if password has been generated, generate if not
if [[ ! -f "$P2_PASSWORD_FILE" ]]; then
    openssl rand -hex 48 > "$P2_PASSWORD_FILE"
fi
# Make sure Password file can only be read by root
chown root: "$P2_PASSWORD_FILE"
chmod 600 "$P2_PASSWORD_FILE"

PASSWORD=$(cat $P2_PASSWORD_FILE)

# Download Helm Chart CRD for k3s, replace values and install
curl -fsSL -o p2_k3s_helm.yaml "https://git.beryju.org/BeryJu.org/p2/raw/version/${P2_VERSION}/install/k3s-helm.yaml"
curl -fsSL -o p2_k3s_storage.yaml "https://git.beryju.org/BeryJu.org/p2/raw/version/${P2_VERSION}/install/k3s-storage.yaml"
curl -fsSL -o p2_k3s_nginx.yaml "https://git.beryju.org/BeryJu.org/p2/raw/version/${P2_VERSION}/install/k3s-nginx-ingress.yaml"
curl -fsSL -o p2_k3s_all_ingress.yaml "https://git.beryju.org/BeryJu.org/p2/raw/version/${P2_VERSION}/install/k3s-all-ingress.yaml"

sed -i "s|%PASSWORD%|${PASSWORD}|g" p2_k3s_helm.yaml
sed -i "s|%STORAGE_BASE%|${STORAGE_BASE}|g" p2_k3s_storage.yaml

# Run docker image pull in foreground to better show progress
docker image pull docker.beryju.org/p2/server:$P2_VERSION
docker image pull docker.beryju.org/p2/tier0:$P2_VERSION
docker image pull bitnami/postgresql:10.6.0
docker image pull bitnami/redis:4.0.11

sleep 30
mv p2_k3s_nginx.yaml /var/lib/rancher/k3s/server/manifests/p2-10-nginx.yaml
sleep 30
mv p2_k3s_storage.yaml /var/lib/rancher/k3s/server/manifests/p2-20-storage.yaml
sleep 30
mv p2_k3s_helm.yaml /var/lib/rancher/k3s/server/manifests/p2-30-helm.yaml
mv p2_k3s_all_ingress.yaml /var/lib/rancher/k3s/server/manifests/p2-31-all-ingress.yaml

echo " * Your p2 instanace will be available on port 443 in a few minutes."
echo " * You can use the username admin with password admin to login."

rm -r "${TEMP_DIR}"
