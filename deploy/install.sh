#!/bin/bash

# p2 Install script
# Installs and updates a p2 instance using k3s and docker

P2_VERSION="0.7.6"

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
curl -sfL https://get.k3s.io -o install.k3s.sh
bash install.k3s.sh > /dev/null 2>&1

STORAGE_BASE="${STORAGE_BASE:-/srv/p2}"
# Make sure storage directories exist
mkdir -p "${STORAGE_BASE}"
curl -fsSL -o p2_k3s_storage.yaml "https://git.beryju.org/BeryJu.org/p2/raw/version/${P2_VERSION}/install/k3s-storage.yaml"
sed -i "s|%STORAGE_BASE%|${STORAGE_BASE}|g" p2_k3s_storage.yaml
mv p2_k3s_storage.yaml /var/lib/rancher/k3s/server/manifests/p2-20-storage.yaml
sleep 30
# TODO: Download crd and operator
# echo " * Your p2 instanace will be available at $INGRESS_HOST in a few minutes."
# echo " * You can use the username admin with password admin to login."

rm -r "${TEMP_DIR}"
