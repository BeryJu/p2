#!/bin/bash

# p2 Install script
# Installs and updates a p2 instance using k3s and docker
# Supported enviormnet variables:
# - INGRESS_HOST: Hostname under which p2 will be available
# - STORAGE_BASE: Base directory in which p2 data will be storeed
# - LE_MAIL: Optional; Let's Encrypt E-Mail. If this is not set, Let's Encrypt is not enabled.

K3S_VERSION="0.4.0"
P2_VERSION="0.3.5"
export INSTALL_K3S_EXEC="--cluster-cidr 10.121.0.0/16 --cluster-domain p2.baked --docker --no-deploy traefik"

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
# curl -fsSL -o p2_k3s_cert.yaml "https://git.beryju.org/BeryJu.org/p2/raw/version/${P2_VERSION}/install/k3s-cert-manager.yaml"

# Replace variable in Helm CRD
sed -i "s|%INGRESS_HOST%|${INGRESS_HOST}|g" p2_k3s_helm.yaml
sed -i "s|%PASSWORD%|${PASSWORD}|g" p2_k3s_helm.yaml

# Replace variable in Storage
sed -i "s|%STORAGE_BASE%|${STORAGE_BASE}|g" p2_k3s_storage.yaml

# Replace variable in cert-manager
# sed -i "s|%LE_MAIL%|${LE_MAIL}|g" p2_k3s_cert.yaml

mv p2_k3s_nginx.yaml /var/lib/rancher/k3s/server/manifests/p2-10-nginx.yaml
mv p2_k3s_storage.yaml /var/lib/rancher/k3s/server/manifests/p2-20-storage.yaml
mv p2_k3s_helm.yaml /var/lib/rancher/k3s/server/manifests/p2-30-helm.yaml

# Only deploy cert-manager if LE_MAIL set
# if [ -n "$LE_MAIL" ]; then
#     mv p2_k3s_cert.yaml /var/lib/rancher/k3s/server/manifests/p2-40-cert.yaml
# fi

echo " * Your p2 instanace will be available at $INGRESS_HOST in a few minutes."
echo " * You can use the username admin with password admin to login."

rm -r "${TEMP_DIR}"
