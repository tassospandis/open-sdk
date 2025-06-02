# -*- coding: utf-8 -*-
import pytest

from src.edgecloud.clients.aeros.client import EdgeApplicationManager as AerosClient
from src.edgecloud.clients.i2edge.client import EdgeApplicationManager as I2EdgeClient

# from src.edgecloud.clients.piedge.client import EdgeApplicationManager as PiEdgeClient
from src.edgecloud.core.edgecloud_factory import EdgeCloudFactory
from tests.edgecloud.test_cases import test_cases


@pytest.mark.parametrize("client_name, base_url", test_cases)
def test_factory_edgecloud(client_name, base_url):
    """
    Test the factory pattern for the edgecloud client.
    """
    client_class_map = {
        "i2edge": I2EdgeClient,
        "aeros": AerosClient,
        # "piedge": PiEdgeClient,
    }
    expected_client_class = client_class_map[client_name]
    edgecloud_platform = EdgeCloudFactory.create_edgecloud_client(client_name, base_url)
    assert isinstance(edgecloud_platform, expected_client_class)
