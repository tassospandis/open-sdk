# -*- coding: utf-8 -*-
import pytest

from src.common.sdk_catalog_client import SdkCatalogClient

NETWORK_TEST_CASES = [
    {
        "network": {
            "client_name": "open5gs",
            "base_url": "http://test-open5gs.url",
            "scs_as_id": "scs1",
        }
    },
    {
        "network": {
            "client_name": "oai",
            "base_url": "http://test-oai.url",
            "scs_as_id": "scs2",
        }
    },
    {
        "network": {
            "client_name": "open5gcore",
            "base_url": "http://test-open5gcore.url",
            "scs_as_id": "scs3",
        }
    },
]


@pytest.mark.parametrize(
    "client_specs", NETWORK_TEST_CASES, ids=["open5gs", "oai", "open5gcore"]
)
def test_network_platform_instantiation(client_specs):
    """Test instantiation of all network platform clients"""
    clients = SdkCatalogClient.create_clients_from(client_specs)

    assert "network" in clients
    network_client = clients["network"]
    assert network_client is not None
    assert "NetworkManager" in str(type(network_client))
