from modules.cluster import ClusterOpsService
from modules.deployment import DeploymentOpsService


def test_deployment_module():
    service = ClusterOpsService()
    for deployment in service.list_all_deployments().items:
        print(deployment.metadata.name)

def test_deployment_module1():
    service = DeploymentOpsService(namespace="default",name="production-app")
    service.get_diagnostic()

