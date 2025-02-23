from modules.cluster import ClusterOpsService
import pytest
from unittest.mock import patch, Mock


@pytest.fixture
def mock_k8s_client():
    with patch('k8s_client.client.CoreV1Api') as mock_v1_api:
        yield mock_v1_api


@patch('kubernetes.config.load_kube_config')
@patch('kubernetes.config.load_incluster_config')
def test_list_all_deployments(mock_client, mock_config):
    ops_object = ClusterOpsService()
    response = ops_object.list_all_deployments()
    assert response
