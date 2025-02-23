from modules.base import K8SOpsService


class PodOpsService(K8SOpsService):
    name: str = ""
    namespace: str = ""

    def __init__(self, name: str = "", namespace: str = ""):
        super().__init__()
        self.name = name
        self.namespace = namespace

    def get_logs(self):
        return self.core_v1_api.read_namespaced_pod_log(
            name=self.name, namespace=self.namespace, tail_lines=20)

    def get_metrics(self):
        metrics = self.metrics_api.list_namespaced_custom_object(
            group="metrics.k8s.io",
            version="v1beta1",
            namespace=self.namespace,
            plural="pods"
        )
        return metrics
