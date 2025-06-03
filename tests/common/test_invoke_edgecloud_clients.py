# -*- coding: utf-8 -*-
import pytest

from src.common.sdk_catalog_client import SdkCatalogClient

EDGE_CLOUD_TEST_CASES = [
    {"edgecloud": {"client_name": "i2edge", "base_url": "http://test-i2edge.url"}},
    {
        "edgecloud": {
            "client_name": "aeros",
            "base_url": "http://test-aeros.url",
            "aerOS_API_URL": "http://fake.api.url",
            "aerOS_ACCESS_TOKEN": "fake-access",
            "aerOS_HLO_TOKEN": "fake-hlo",
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


@pytest.mark.parametrize(
    "client_specs",
    EDGE_CLOUD_TEST_CASES,
    ids=[
        "i2edge",
        "aeros",
        # "piedge"
    ],
)
def test_edgecloud_platform_instantiation(client_specs):
    """Test instantiation of all edgecloud platform clients"""
    clients = SdkCatalogClient.create_clients_from(client_specs)

    assert "edgecloud" in clients
    edge_client = clients["edgecloud"]
    assert edge_client is not None
    assert "EdgeApplicationManager" in str(type(edge_client))
