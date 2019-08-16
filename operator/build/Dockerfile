# Since kaniko seems to have issues with quay.io for some reason, the image is replicated to docker.beryju.org
FROM docker.beryju.org/k8s/helm-operator:v0.8.1

COPY watches.yaml ${HOME}/watches.yaml
COPY helm-charts/ ${HOME}/helm-charts/
