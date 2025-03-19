import pytest

from src.edgecloud.core.edgecloud_factory import EdgeCloudFactory
from src.edgecloud.clients.i2edge.client import EdgeApplicationManager as I2EdgeClient
from src.edgecloud.clients.aeros.client import EdgeApplicationManager as AerosClient
from src.edgecloud.clients.piedge.client import EdgeApplicationManager as PiEdgeClient
from src.edgecloud.clients.dmo.client import EdgeApplicationManager as DmoClient

# Define common test cases for all tests
test_cases = [
    ("i2edge", "http://192.168.123.237:30769/"),
    ("aeros", "http://aeros.example.com/"),
    ("piedge", "http://piedge.example.com/"),
    ("dmo", "http://dmo.example.com/")
]

# Add an invalid client test case
invalid_test_case = [("invalid_client", "http://invalid.url/")]


@pytest.mark.parametrize("client_name, base_url", test_cases)
def test_factory_edgecloud(client_name, base_url):
    """
    Test the factory pattern for the edgecloud client.
    """
    # Map client names to their corresponding client classes
    client_class_map = {
        "i2edge": I2EdgeClient,
        "aeros": AerosClient,
        "piedge": PiEdgeClient,
        "dmo": DmoClient,
    }

    expected_client_class = client_class_map[client_name]
    edgecloud_platform = EdgeCloudFactory.create_edgecloud_client(client_name, base_url)
    assert isinstance(edgecloud_platform, expected_client_class)


@pytest.mark.parametrize("client_name, base_url", test_cases)
def test_get_edge_cloud_zones_return_list(client_name, base_url):
    """
    Test the get_edge_cloud_zones method for each client.
    """
    # Create the edgecloud client
    edgecloud_platform = EdgeCloudFactory.create_edgecloud_client(client_name, base_url)

    # Call the get_edge_cloud_zones function
    zones = edgecloud_platform.get_edge_cloud_zones()

    # Assert that the result is a list (or whatever the expected type is)
    assert isinstance(zones, list), f"Expected a list of zones for {client_name}, but got {type(zones)}"
