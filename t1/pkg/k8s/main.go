package k8s

import (
	"errors"
	"io/ioutil"

	log "github.com/sirupsen/logrus"
	v1 "k8s.io/api/core/v1"
	metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
	"k8s.io/apimachinery/pkg/labels"
	"k8s.io/client-go/kubernetes"
	"k8s.io/client-go/rest"
)

type KubernetesContext struct {
	*kubernetes.Clientset
	Namespace string
	Logger    *log.Entry
}

// NewKubernetesContext Connect to kubernetes cluster
func NewKubernetesContext() (KubernetesContext, error) {
	logger := log.WithFields(log.Fields{
		"component": "k8s",
	})
	logger.Debug("Attempting to use InClusterConfig...")
	// creates the in-cluster config
	config, err := rest.InClusterConfig()
	if err != nil {
		logger.Warning(err)
		return KubernetesContext{}, err
	}
	// creates the clientset
	clientset, err := kubernetes.NewForConfig(config)
	if err != nil {
		logger.Warning(err)
		return KubernetesContext{}, err
	}
	// Since we can't get the namespace directly, we have to try and read /var/run/secrets/kubernetes.io/serviceaccount/namespace
	namespaceBytes, err := ioutil.ReadFile("/var/run/secrets/kubernetes.io/serviceaccount/namespace")
	if err != nil {
		logger.Warning(err)
		return KubernetesContext{}, err
	}
	namespace := string(namespaceBytes)
	logger.Debugf("Detected current namespace: %s", namespace)
	return KubernetesContext{clientset, namespace, logger}, nil
}

// PodsForComponent get all pods which belong to component, used for Cache Peers
func (k8sc *KubernetesContext) PodsForComponent(component string) *v1.PodList {
	labelSelector := metav1.LabelSelector{MatchLabels: map[string]string{"k8s.p2.io/component": component}}
	pods, err := k8sc.CoreV1().Pods(k8sc.Namespace).List(metav1.ListOptions{
		LabelSelector: labels.Set(labelSelector.MatchLabels).String(),
	})
	if err != nil {
		k8sc.Logger.Warning(err)
		return nil
	}
	return pods
}

// WebClusterIP Get ClusterIP to access p2 server
func (k8sc *KubernetesContext) WebClusterIP() (string, error) {
	labelSelector := metav1.LabelSelector{MatchLabels: map[string]string{"k8s.p2.io/component": "web"}}
	services, err := k8sc.CoreV1().Services(k8sc.Namespace).List(metav1.ListOptions{
		LabelSelector: labels.Set(labelSelector.MatchLabels).String(),
	})
	if err != nil {
		k8sc.Logger.Warning(err)
		return "", err
	}
	if services.Size() < 1 {
		err := errors.New("No Service found")
		k8sc.Logger.Warning(err)
		return "", err
	}
	k8sc.Logger.Debugf("Found p2 web ClusterIP: %s", services.Items[0].Spec.ClusterIP)
	return services.Items[0].Spec.ClusterIP, nil
}
