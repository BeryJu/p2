#!/bin/bash

# p2 Install script
# Installs and updates a p2 instance using k3s and docker

# TODO: Check if root

K3S_VERSION="v0.4.0"

# Check if docker installed
curl "https://get.docker.com" | sh -
# Check if k3s installed
curl "https://raw.githubusercontent.com/rancher/k3s/${K3S_VERSION}/install.sh" | INSTALL_K3S_EXEC="--cluster-cidr 10.121.0.0/16 --cluster-domain p2.baked --docker" sh -

P2_STORAGE_PATH="/srv/p2/storage/"
P2_DATABASE_PATH="/srv/p2/database/"

mkdir -p $P2_STORAGE_PATH
mkdir -p $P2_DATABASE_PATH

echo <<EOF > /var/lib/rancher/k3s/server/manifests/p2-storage.yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: p2-pv-app-storage
spec:
  capacity:
    storage: 100Gi
  accessModes:
  - ReadWriteOnce
  claimRef:
    namespace: p2
    name: p2-pvc-app-storage
  storageClassName: standard
  hostPath:
    path: ${P2_STORAGE_PATH}
---
apiVersion: v1
kind: PersistentVolume
metadata:
  name: p2-pv-postgresql
spec:
  capacity:
    storage: 100Gi
  accessModes:
  - ReadWriteOnce
  claimRef:
    namespace: p2
    name: p2-pvc-postgresql
  storageClassName: standard
  hostPath:
    path: ${P2_DATABASE_PATH}
---
kind: PersistentVolumeClaim
apiVersion: v1
metadata:
  name: p2-pvc-app-storage
spec:
  storageClassName: standard
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 100Gi
---
kind: PersistentVolumeClaim
apiVersion: v1
metadata:
  name: p2-pvc-postgresql
spec:
  storageClassName: standard
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 100Gi
EOF