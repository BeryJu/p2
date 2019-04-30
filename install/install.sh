#!/bin/bash

# p2 Install script
# Installs and updates a p2 instance using k3s and docker
# Supported enviormnet variables:
# - INGRESS_HOST: Hostname under which p2 will be available
# - STORAGE_BASE: Base directory in which p2 data will be storeed

K3S_VERSION="0.4.0"
P2_VERSION="0.1.7"

if [ "$EUID" -ne 0 ]; then
    echo "Please run as root"
    exit
fi

# Make sure docker is installed
curl "https://get.docker.com" | sh - >/dev/null 2>&1
# Make sure K3s is installed
export INSTAL_LK3S_EXEC="--cluster-cidr 10.121.0.0/16 --cluster-domain p2.baked --docker"
curl "https://raw.githubusercontent.com/rancher/k3s/v${K3S_VERSION}/install.sh" |  sh - >/dev/null 2>&1

P2_STORAGE_PATH="${STORAGE_BASE:-/srv/p2}/storage/"
P2_DATABASE_PATH="${STORAGE_BASE:-/srv/p2}/database/"
P2_PASSWORD_FILE="${STORAGE_BASE:-/srv/p2}/password"

# Make sure storage directories exist
mkdir -p $P2_STORAGE_PATH
mkdir -p $P2_DATABASE_PATH

# Check if password has been generated, generate if not
if [[ ! -f "$P2_PASSWORD_FILE" ]]; then
    openssl rand 30 -base64 > "$P2_PASSWORD_FILE"
fi
PASSWORD=$(cat $P2_PASSWORD_FILE)

# Download Helm Chart CRD for k3s, replace values and install
wget -O /tmp/p2_k3s_helm.yml "https://git.beryju.org/BeryJu.org/p2/raw/version/${P2_VERSION}/install/k3s-helm.yaml"
wget -O /tmp/p2_k3s_storage.yml "https://git.beryju.org/BeryJu.org/p2/raw/version/${P2_VERSION}/install/k3s-storage.yaml"

# Replace variable in Helm CRD
sed -i "s/%INGRESS_HOST%/${INGRESS_HOST}/g" /tmp/p2_k3s_helm.yml
sed -i "s/%PASSWORD%/${PASSWORD}/g" /tmp/p2_k3s_helm.yml

# Replace variable in Storage
sed -i "s/%P2_STORAGE_PATH%/${P2_STORAGE_PATH}/g" /tmp/p2_k3s_storage.yml
sed -i "s/%P2_DATABASE_PATH%/${P2_DATABASE_PATH}/g" /tmp/p2_k3s_storage.yml

mv /tmp/p2_k3s_storage.yml /var/lib/rancher/k3s/server/manifests/p2.yaml
mv /tmp/p2_k3s_helm.yml /var/lib/rancher/k3s/server/manifests/p2.yaml

echo " * Your p2 instanace will be available at $INGRESS_HOST in a few minutes."
echo " * You can use the username admin with password admin to login."
