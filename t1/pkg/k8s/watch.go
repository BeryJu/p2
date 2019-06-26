package k8s

import (
	v1 "k8s.io/api/core/v1"
	"k8s.io/apimachinery/pkg/fields"
	"k8s.io/client-go/tools/cache"
)

func (k8sc *KubernetesContext) podIsCache(pod v1.Pod) bool {
	if val, ok := pod.Labels["k8s.p2.io/component"]; ok {
		return val == "cache"
	}
	return false
}

// WatchNewCachePods Watch K8s API for pod changes and refresh peers
func (k8sc *KubernetesContext) WatchNewCachePods(stop chan struct{}, updateFunc func(pod v1.Pod)) {
	watchlist := cache.NewListWatchFromClient(
		k8sc.CoreV1().RESTClient(),
		string(v1.ResourcePods),
		k8sc.Namespace,
		fields.Everything(),
	)
	_, controller := cache.NewInformer( // also take a look at NewSharedIndexInformer
		watchlist,
		&v1.Pod{},
		0, //Duration is int64
		cache.ResourceEventHandlerFuncs{
			AddFunc: func(obj interface{}) {
				if pod, ok := obj.(*v1.Pod); ok {
					if k8sc.podIsCache(*pod) {
						updateFunc(*pod)
					}
				}
			},
			DeleteFunc: func(obj interface{}) {
				if pod, ok := obj.(*v1.Pod); ok {
					if k8sc.podIsCache(*pod) {
						updateFunc(*pod)
					}
				}
			},
			UpdateFunc: func(oldObj, newObj interface{}) {
				if pod, ok := newObj.(*v1.Pod); ok {
					if k8sc.podIsCache(*pod) {
						updateFunc(*pod)
					}
				}
			},
		},
	)
	// I found it in k8s scheduler module. Maybe it's help if you interested in.
	// serviceInformer :=
	// cache.NewSharedIndexInformer(watchlist,
	//  &v1.Service{}, 0, cache.Indexers{
	//     cache.NamespaceIndex: cache.MetaNamespaceIndexFunc,
	// })
	// go serviceInformer.Run(stop)
	k8sc.Logger.Debug("Watching for Pod changes...")
	controller.Run(stop)
}
