from modules.base import K8SOpsService


class NamespaceOpsService(K8SOpsService):
    namespace_name: str

    def __init__(self, namespace_name: str):
        super().__init__()
        self.namespace_name = namespace_name

    def list_namespaced(self):
        return self.api_client.list_namespaced_deployment(self.namespace_name)
