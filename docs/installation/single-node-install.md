# Single-Node Installation

Since p2 is built with Kubernetes integration, the only supported method to run p2 is within such a cluster. To run p2 on a single node, it is recommended to use [k3s](https://k3s.io). This page is a short guide on how to prepare your single node for p2.

## Requirements

### Hardware

|  | With tier0 | Without tier0 |
|--|------------|---------------|
| CPU | 2 Cores | 2 Cores |
| RAM | 2 GB | 4 GB |
| Disk | At least 20 GB recommended + your data |

## Installing k3s

Installing k3s is very easy. Simply run the following script on your node to install the Cluster.

```
curl -sfL https://get.k3s.io | sh -
```

After the script is done, you should be able to run `kubectl get node` and see one ready node:

```
NAME         STATUS   ROLES    AGE   VERSION
p2-test-vm   Ready    master   13s   v1.14.5-k3s.1
```

Congratulations, you now have a single-node Kubernetes cluster. By default, k3s installs traefik as `Ingress Controller` (= Reverse Proxy). There is however no default Persistent Volume Provisioner, which means we need the following component:

## Installing local-path-provisioner

This tool allows Kubernetes to dynamically allocate "Volumes", pointing to a local path. Download the install-manifest as following:

```
wget https://raw.githubusercontent.com/rancher/local-path-provisioner/master/deploy/local-path-storage.yaml
```

The default base-path is `/opt/local-path-provisioner`. If you wish to change that path, download the YAML file and edit it to your needs.

Once you're done, apply the manifest with this command: `kubectl apply -f local-path-storage.yaml`.

To check that the provisioner has successfully been installed and is running, execture `kubectl -n local-path-storage get pod`. The output should look something like this:

```
NAME                                    READY   STATUS    RESTARTS   AGE
local-path-provisioner-848fdcff-h4l68   1/1     Running   0          10s
```

By default, the local-path-provisioner is not set as default. To change that, run

```
kubectl patch storageclass local-path -p '{"metadata": {"annotations":{"storageclass.kubernetes.io/is-default-class":"true"}}}'
```

Now that you have a fully-prepared Kubernetes cluster, you can continue with the normal Installation instructions [here](install.md)
