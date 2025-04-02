import pytest

from src.edgecloud.core.edgecloud_factory import EdgeCloudFactory
from src.edgecloud.clients.errors import EdgeCloudPlatformError
from tests.edgecloud.test_cases import test_cases


@pytest.mark.parametrize("client_name, base_url", test_cases)
def test_get_edge_cloud_zones(client_name, base_url):
    """
    Test the format of the response from get_edge_cloud_zones for each client.
    """
    edgecloud_platform = EdgeCloudFactory.create_edgecloud_client(
        client_name, base_url
    )

    try:
        zones = edgecloud_platform.get_edge_cloud_zones()
        assert isinstance(zones, list)
        for zone in zones:
            assert "zoneId" in zone
            assert "geographyDetails" in zone
    except EdgeCloudPlatformError as e:
        pytest.fail(f"Failed to retrieve zones: {e}")
