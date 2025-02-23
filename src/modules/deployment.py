from datetime import datetime

from kubernetes.client import ApiException
from modules.base import K8SOpsService


class DeploymentDiagnosticInfo:
    def __init__(self, deployment):
        self.name = deployment.metadata.name
        self.namespace = deployment.metadata.namespace
        self.replicas = deployment.spec.replicas
        self.available_replicas = deployment.status.available_replicas or 0
        self.unavailable_replicas = self.replicas - self.available_replicas
        self.strategy = deployment.spec.strategy.type
        self.labels = deployment.metadata.labels

    def to_list(self):
        return [
            self.name,
            self.namespace,
            self.replicas,
            self.available_replicas,
            self.unavailable_replicas,
            self.strategy,
            self.labels,
        ]


class DeploymentOpsService(K8SOpsService):
    name: str = ""
    namespace: str = ""

    def __init__(self, name: str, namespace: str = ""):
        super().__init__()
        self.name = name
        self.namespace = namespace

    def scale_deployment(self, replicas):
        try:
            scale_body = {
                "spec": {
                    "replicas": replicas
                }
            }

            self.api_client.patch_namespaced_deployment_scale(
                name=self.name,
                namespace=self.namespace,
                body=scale_body
            )
            return f"Deployment {self.name} scaled to {replicas} replicas."
        except ApiException as e:
            raise Exception(f"Failed to scale deployment {self.name} in namespace {self.namespace}: Reason {e.reason}")

    def get_info(self):
        try:
            deployment = self.api_client.read_namespaced_deployment(
                name=self.name,
                namespace=self.namespace
            )
            return deployment
        except ApiException as e:
            raise Exception(f"Failed to get deployment {self.name} in namespace {self.namespace}: {e}")

    def get_diagnostic(self):
        deployment = self.api_client.read_namespaced_deployment(
            name=self.name,
            namespace=self.namespace)
        return DeploymentDiagnosticInfo(deployment)

    def get_pods(self):
        deployment = self.get_info()
        label_selector = deployment.spec.selector.match_labels
        label_selector_str = ",".join([f"{key}={value}" for key, value in label_selector.items()])
        pods = self.core_v1_api.list_namespaced_pod(
            namespace=self.namespace,
            label_selector=label_selector_str
        )
        return pods

    def get_logs(self, name: str, namespace: str = ""):
        pass
