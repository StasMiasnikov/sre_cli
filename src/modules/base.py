from kubernetes import client, config
from kubernetes.client import AppsV1Api, CoreV1Api, CustomObjectsApi
from kubernetes.client.rest import ApiException


class K8SOpsService:
    api_client: AppsV1Api = None
    core_v1_api: CoreV1Api = None
    metrics_api: CustomObjectsApi = None

    def __init__(self):
        try:
            config.load_kube_config()
        except ApiException as e:
            raise Exception(f"Failed to load kubeconfig: {e}")
        self.api_client = client.AppsV1Api()
        self.core_v1_api = client.CoreV1Api()
        self.metrics_api = client.CustomObjectsApi()
