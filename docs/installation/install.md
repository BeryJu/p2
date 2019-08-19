# Installation

This guide expects you to have a fully-configured Kubernetes cluster. If you want to run p2 on a single server, read [this](single-node-install.md) first.

## Operator

p2 uses an operator to manage itself. Execute `kubectl apply -f https://git.beryju.org/BeryJu.org/p2/raw/master/deploy/operator.yaml` to install the Operator.

To verify that the operator has successfully been installed and is running, check the output of `kubectl get pod`.

```
NAME                           READY   STATUS    RESTARTS   AGE
p2-operator-5bc6bcf5c7-qtsp2   1/1     Running   0          98s
```

## Instance

Now to create the actual p2 instance, download the [example](https://git.beryju.org/BeryJu.org/p2/raw/master/deploy/example-instance.yaml) instance definition and change it to your needs.

After you've change the YAML to your liking, create the instance with the following command:

```
kubectl apply -f example-instance.yaml
```

The actually bootstrapping of the instance can take a few minutes. Run this command to watch the progress: `watch kubectl get pods`

Once the output looks something like this, your p2 install is ready to use.

```
NAME                                                              READY   STATUS    RESTARTS   AGE
example-p2-18vtwme7xxcdin9copwgnnz13-grpc-b76c8b87c-jhv98         1/1     Running   0          10m
example-p2-18vtwme7xxcdin9copwgnnz13-postgresql-0                 1/1     Running   0          10m
example-p2-18vtwme7xxcdin9copwgnnz13-redis-master-0               1/1     Running   0          10m
example-p2-18vtwme7xxcdin9copwgnnz13-redis-slave-776bd5569h7ttx   1/1     Running   0          10m
example-p2-18vtwme7xxcdin9copwgnnz13-static-659f977dc4-8sx5m      2/2     Running   0          10m
example-p2-18vtwme7xxcdin9copwgnnz13-tier0-77f7694798-4d776       1/1     Running   0          10m
example-p2-18vtwme7xxcdin9copwgnnz13-tier0-77f7694798-f5tc9       1/1     Running   0          10m
example-p2-18vtwme7xxcdin9copwgnnz13-web-77f44bd466-ngslj         1/1     Running   0          10m
example-p2-18vtwme7xxcdin9copwgnnz13-worker-6c69d985b-l8vdd       1/1     Running   0          10m
p2-operator-5bc6bcf5c7-qtsp2                                      1/1     Running   0          34m
```

Access your p2 install under the domain(s) configured. The default login credentials are `admin/admin`.
