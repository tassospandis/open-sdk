# -*- coding: utf-8 -*-
import pytest

from sunrise6g_opensdk.common.sdk import Sdk as sdkclient

EDGE_CLOUD_TEST_CASES = [
    {
        "edgecloud": {
            "client_name": "i2edge",
            "base_url": "http://test-nbi-i2edge.sunrise6g",
        }
    },
    {
        "edgecloud": {
            "client_name": "aeros",
            "base_url": "https://ncsrd-mvp-domain.aeros-project.eu",
            # Additional parameters for aerOS client:
            "aerOS_API_URL": "https://ncsrd-mvp-domain.aeros-project.eu",
            "aerOS_ACCESS_TOKEN": "eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJzaTcxSzNkUm11UFIxY2RhT2daNVFtbGpUVlR6U3JQM0cyYlZNdEVDeUVjIn0.eyJleHAiOjE4MTcwMzUwMTksImlhdCI6MTczMDcyMTQxOSwianRpIjoiODk2ODhlODktNTRmOS00MzFhLTliZTUtOTQ5MmMxYjE0NDZiIiwiaXNzIjoiaHR0cHM6Ly9rZXljbG9hay5jZi1tdnAtZG9tYWluLmFlcm9zLXByb2plY3QuZXUvYXV0aC9yZWFsbXMva2V5Y2xvYWNrLW9wZW5sZGFwIiwiYXVkIjoiYWNjb3VudCIsInN1YiI6ImE5ZWY0ZTFiLTg5NTgtNGZkYS1hODQ5LTJlNjdlZmY3NjkzMyIsInR5cCI6IkJlYXJlciIsImF6cCI6ImFlcm9zLXRlc3QiLCJzZXNzaW9uX3N0YXRlIjoiOGM2MTJjMDYtYTE5MS00MjBmLTlmNTItZGU5OWZiYzJkODI3IiwiYWNyIjoiMSIsInJlYWxtX2FjY2VzcyI6eyJyb2xlcyI6WyJDbG91ZEZlcnJvRG9tYWluIiwiZGVmYXVsdC1yb2xlcy1rZXljbG9hY2stb3BlbmxkYXAiLCJvZmZsaW5lX2FjY2VzcyIsIklvVCBzZXJ2aWNlIGRlcGxveWVyIiwidW1hX2F1dGhvcml6YXRpb24iXX0sInJlc291cmNlX2FjY2VzcyI6eyJhY2NvdW50Ijp7InJvbGVzIjpbIm1hbmFnZS1hY2NvdW50IiwibWFuYWdlLWFjY291bnQtbGlua3MiLCJ2aWV3LXByb2ZpbGUiXX19LCJzY29wZSI6InByb2ZpbGUgZW1haWwiLCJzaWQiOiI4YzYxMmMwNi1hMTkxLTQyMGYtOWY1Mi1kZTk5ZmJjMmQ4MjciLCJlbWFpbF92ZXJpZmllZCI6ZmFsc2UsIm5hbWUiOiJJb1Qgc2VydmljZSBkZXBsb3llciAxIERlcGxveWVyIiwicHJlZmVycmVkX3VzZXJuYW1lIjoiaW90c2VydmljZWRlcGxveWVyMSIsImdpdmVuX25hbWUiOiJJb1Qgc2VydmljZSBkZXBsb3llciAxIiwiZmFtaWx5X25hbWUiOiJEZXBsb3llciJ9.XXM3HYVntCrSOsyJIKg-ATsqMigyQZhLMaeZtl9GqYPuISXfYl3AV0Hcs5w3n55J_-NOdlFnZdJgHlpEdB9LvxegagI4ZteoEZC72og9OdmzFV1ud4jPTrhGm7rbjCXs7bF-sGwGCKrLIs53PZPQiRcm1KxfN4RhBy3sL0Ff79QHkgvTbag-DQMrh5Y_NrTifrMrZ0i8JZD8AsRrHoi5zs7N2PXQ0zNv3n1dxxlWBKd46cWh3kutqNgTNV-s7YTde1FCSthKMcQLxe284qdFWAYlctzU5y4zLe-3VPxU7fH16jD7yAazTYdGVy4U0B5fPn_087ABjEf0oZmt40nuug",
            "aerOS_HLO_TOKEN": "eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJzaTcxSzNkUm11UFIxY2RhT2daNVFtbGpUVlR6U3JQM0cyYlZNdEVDeUVjIn0.eyJleHAiOjE4MTcwMzUwMTksImlhdCI6MTczMDcyMTQxOSwianRpIjoiODk2ODhlODktNTRmOS00MzFhLTliZTUtOTQ5MmMxYjE0NDZiIiwiaXNzIjoiaHR0cHM6Ly9rZXljbG9hay5jZi1tdnAtZG9tYWluLmFlcm9zLXByb2plY3QuZXUvYXV0aC9yZWFsbXMva2V5Y2xvYWNrLW9wZW5sZGFwIiwiYXVkIjoiYWNjb3VudCIsInN1YiI6ImE5ZWY0ZTFiLTg5NTgtNGZkYS1hODQ5LTJlNjdlZmY3NjkzMyIsInR5cCI6IkJlYXJlciIsImF6cCI6ImFlcm9zLXRlc3QiLCJzZXNzaW9uX3N0YXRlIjoiOGM2MTJjMDYtYTE5MS00MjBmLTlmNTItZGU5OWZiYzJkODI3IiwiYWNyIjoiMSIsInJlYWxtX2FjY2VzcyI6eyJyb2xlcyI6WyJDbG91ZEZlcnJvRG9tYWluIiwiZGVmYXVsdC1yb2xlcy1rZXljbG9hY2stb3BlbmxkYXAiLCJvZmZsaW5lX2FjY2VzcyIsIklvVCBzZXJ2aWNlIGRlcGxveWVyIiwidW1hX2F1dGhvcml6YXRpb24iXX0sInJlc291cmNlX2FjY2VzcyI6eyJhY2NvdW50Ijp7InJvbGVzIjpbIm1hbmFnZS1hY2NvdW50IiwibWFuYWdlLWFjY291bnQtbGlua3MiLCJ2aWV3LXByb2ZpbGUiXX19LCJzY29wZSI6InByb2ZpbGUgZW1haWwiLCJzaWQiOiI4YzYxMmMwNi1hMTkxLTQyMGYtOWY1Mi1kZTk5ZmJjMmQ4MjciLCJlbWFpbF92ZXJpZmllZCI6ZmFsc2UsIm5hbWUiOiJJb1Qgc2VydmljZSBkZXBsb3llciAxIERlcGxveWVyIiwicHJlZmVycmVkX3VzZXJuYW1lIjoiaW90c2VydmljZWRlcGxveWVyMSIsImdpdmVuX25hbWUiOiJJb1Qgc2VydmljZSBkZXBsb3llciAxIiwiZmFtaWx5X25hbWUiOiJEZXBsb3llciJ9.XXM3HYVntCrSOsyJIKg-ATsqMigyQZhLMaeZtl9GqYPuISXfYl3AV0Hcs5w3n55J_-NOdlFnZdJgHlpEdB9LvxegagI4ZteoEZC72og9OdmzFV1ud4jPTrhGm7rbjCXs7bF-sGwGCKrLIs53PZPQiRcm1KxfN4RhBy3sL0Ff79QHkgvTbag-DQMrh5Y_NrTifrMrZ0i8JZD8AsRrHoi5zs7N2PXQ0zNv3n1dxxlWBKd46cWh3kutqNgTNV-s7YTde1FCSthKMcQLxe284qdFWAYlctzU5y4zLe-3VPxU7fH16jD7yAazTYdGVy4U0B5fPn_087ABjEf0oZmt40nuug",
        }
    },
    # Uncomment once piedge import issues are fixed
    # {
    #     "edgecloud": {
    #         "client_name": "piedge",
    #         "base_url": "http://test-piedge.url"
    #     }
    # }
]


def id_func(val):
    return val["edgecloud"]["client_name"]


@pytest.mark.parametrize("client_specs", EDGE_CLOUD_TEST_CASES, ids=id_func)
def test_edgecloud_platform_instantiation(client_specs):
    """Test instantiation of all edgecloud platform clients"""
    clients = sdkclient.create_clients_from(client_specs)

    assert "edgecloud" in clients
    edge_client = clients["edgecloud"]
    assert edge_client is not None
    assert "EdgeApplicationManager" in str(type(edge_client))
