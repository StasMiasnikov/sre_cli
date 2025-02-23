import inspect
from contextlib import contextmanager
import typer
from typer.core import TyperCommand
from modules.cluster import ClusterOpsService
from modules.deployment import DeploymentOpsService
from modules.namespace import NamespaceOpsService
from tabulate import tabulate

from modules.pod import PodOpsService


@contextmanager
def exception_handler():
    try:
        yield
    except Exception as e:
        typer.echo(f"An error occurred: {e}")


class CliWrapper(TyperCommand):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def invoke(self, ctx):
        with open('cmd.log', 'a') as log_file:
            log_file.write(f"Running command...[{ctx.command.name}] with {ctx.params}\n")
        with exception_handler():
            return super().invoke(ctx)


app = typer.Typer()


@app.command(name="list", cls=CliWrapper)
def cmd_list(namespace: str = typer.Option(default=None, metavar="--namespace",
                                           help="The namespace to list resources from.")):
    if not namespace:
        typer.echo(f"Fetching all deployments")
        response = ClusterOpsService().list_all_deployments()
    else:
        typer.echo(f"Fetching deployment from  namespace {namespace}")
        response = NamespaceOpsService(namespace_name=namespace).list_namespaced()

    table_headers = ["NAME", "READY", "STATUS", "CREATED"]
    data = []
    for deployment_item in response.items:
        data.append([
            deployment_item.metadata.name,
            deployment_item.status.ready_replicas,
            deployment_item.status.conditions[0].type,
            deployment_item.metadata.creation_timestamp
        ])
    typer.echo(tabulate(data, headers=table_headers, tablefmt="plain"))


@app.command(name="scale", cls=CliWrapper)
def cmd_scale(
        replicas: int = typer.Option(default=..., help="Target replicas number", show_default=False),
        deployment: str = typer.Option(default=..., help="Deployment name",
                                       show_default=False),
        namespace: str = typer.Option(None, "--namespace", help="Namespace",
                                      show_default=False)
):
    if not namespace:
        namespace = ClusterOpsService().search_deployments(deployment)

    DeploymentOpsService(
        namespace=namespace, name=deployment
    ).scale_deployment(replicas)
    typer.echo(f"Deployment {deployment} scaled to {replicas} replicas")


@app.command(name="info", cls=CliWrapper)
def cmd_info(
        deployment: str = typer.Option(default=..., help="Deployment name",
                                       show_default=False),
        namespace: str = typer.Option(None, help="Namespace",
                                      show_default=False)):
    if not namespace:
        namespace = ClusterOpsService().search_deployments(deployment)
    deployment_service = DeploymentOpsService(
        namespace=namespace, name=deployment
    )
    table_headers = ["NAME", "REPLICAS", "STATUS", "STRATEGY", "CREATED"]
    deployment_info = deployment_service.get_info()
    data = [
        deployment_info.metadata.name,
        deployment_info.status.ready_replicas,
        deployment_info.status.conditions[0].type,
        deployment_info.spec.strategy.type,
        deployment_info.metadata.creation_timestamp
    ]
    typer.echo(tabulate([data], headers=table_headers, tablefmt="plain"))


@app.command(name="diagnostic", cls=CliWrapper)
def cmd_diagnostic(deployment: str = typer.Option(default=..., help="Deployment name",
                                                  show_default=False),
                   namespace: str = typer.Option(None, help="Namespace",
                                                 show_default=False),
                   pod: str = typer.Option(None, help="Include pod-level diagnostic",
                                           show_default=False),

                   ):
    if not namespace:
        namespace = ClusterOpsService().search_deployments(deployment)
    deployment_service = DeploymentOpsService(
        namespace=namespace, name=deployment
    )

    deployment_pods = deployment_service.get_pods()
    for pod in deployment_pods.items:
        print(pod.metadata.name)
        pod_metrics = PodOpsService(namespace=namespace, name=pod.metadata.name).get_metrics()
        print(pod_metrics)
