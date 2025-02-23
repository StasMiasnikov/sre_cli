from modules.base import K8SOpsService


class ClusterOpsService(K8SOpsService):

    def __init__(self):
        super().__init__()

    def list_all_deployments(self):
        return self.api_client.list_deployment_for_all_namespaces()

    def search_deployments(self, deployment_name: str):
        deployments = self.api_client.list_deployment_for_all_namespaces()
        namespace: str = ""
        for deployment in deployments.items:
            if deployment.metadata.name == deployment_name:
                namespace = deployment.metadata.namespace
        if not namespace:
            raise Exception(f"Deployment {deployment_name} not found")
        return namespace
