#!/bin/bash

# p2 Install script
# Installs and updates a p2 instance using k3s and docker
# Supported enviormnet variables:
# - INGRESS_HOST: Hostname under which p2 will be available
# - STORAGE_BASE: Base directory in which p2 data will be storeed

K3S_VERSION="0.4.0"
P2_VERSION="0.1.16"
export INSTALL_K3S_EXEC="--cluster-cidr 10.121.0.0/16 --cluster-domain p2.baked --docker"
export INSTALL_K3S_EXEC="--cluster-cidr 10.121.0.0/16 --cluster-domain p2.baked --docker --no-deploy traefik"

if [ "$EUID" -ne 0 ]; then
    echo "Please run as root"
    exit
fi

# Create temporary folder and cd to it
TEMP_DIR=$(mktemp -d --suffix _p2)
cd "${TEMP_DIR}"

# Make sure docker is installed
curl -fsSL https://get.docker.com -o install.docker.sh
bash install.docker.sh > /dev/null 2>&1
# Make sure K3s is installed
curl -fsSL "https://raw.githubusercontent.com/rancher/k3s/v${K3S_VERSION}/install.sh" -o install.k3s.sh
bash install.k3s.sh > /dev/null 2>&1

P2_STORAGE_PATH="${STORAGE_BASE:-/srv/p2}/storage/"
P2_DATABASE_PATH="${STORAGE_BASE:-/srv/p2}/database/"
P2_PASSWORD_FILE="${STORAGE_BASE:-/srv/p2}/password"

# Make sure storage directories exist
mkdir -p $P2_STORAGE_PATH
mkdir -p $P2_DATABASE_PATH

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

# Replace variable in Helm CRD
sed -i "s|%INGRESS_HOST%|${INGRESS_HOST}|g" p2_k3s_helm.yaml
sed -i "s|%PASSWORD%|${PASSWORD}|g" p2_k3s_helm.yaml

# Replace variable in Storage
sed -i "s|%P2_STORAGE_PATH%|${P2_STORAGE_PATH}|g" p2_k3s_storage.yaml
sed -i "s|%P2_DATABASE_PATH%|${P2_DATABASE_PATH}|g" p2_k3s_storage.yaml

mv p2_k3s_nginx.yaml /var/lib/rancher/k3s/server/manifests/p2-10-nginx.yaml
mv p2_k3s_storage.yaml /var/lib/rancher/k3s/server/manifests/p2-20-storage.yaml
mv p2_k3s_helm.yaml /var/lib/rancher/k3s/server/manifests/p2-30-helm.yaml

echo " * Your p2 instanace will be available at $INGRESS_HOST in a few minutes."
echo " * You can use the username admin with password admin to login."

rm -r "${TEMP_DIR}"
