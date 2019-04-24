## Kubernetes

The recommended way to deploy p2 on docker is on Kubernetes. To make installation easier, we provide a helm chart for this.

To install p2 using helm on kubernetes, run the following:

```
helm repo add beryju.org https://pkg.beryju.org/repository/helm/
helm install beryju.org/p2
```

## Pure Docker

p2 can be run on pure docker. The image is `docker.pkg.beryju.org/p2`. The image needs to be run twice, once for the webserver and once for the background worker. The config file needs to be mounted under `/etc/p2/config.yml`. Uploaded files are saved under `/storage`, which should be mounted as well.

The webserver can be started by running `manage.py web` in the Container. The process will listen on port 8000 for incoming connections.
The background-worker can be started by running `manage.py worker`.
