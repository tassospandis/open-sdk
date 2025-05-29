# -*- coding: utf-8 -*-
import pytest

from src.edgecloud.clients.errors import EdgeCloudPlatformError
from src.edgecloud.core.edgecloud_factory import EdgeCloudFactory
from tests.edgecloud.test_cases import test_cases

zone_id = "Omega12345"


@pytest.mark.parametrize("client_name, base_url", test_cases)
def test_get_edge_cloud_zones(client_name, base_url):
    """
    Test the format of the response from get_edge_cloud_zones for each client.
    """
    edgecloud_platform = EdgeCloudFactory.create_edgecloud_client(client_name, base_url)
    try:
        zones = edgecloud_platform.get_edge_cloud_zones()
        assert isinstance(zones, list)
        for zone in zones:
            assert "zoneId" in zone
            assert "geographyDetails" in zone
    except EdgeCloudPlatformError as e:
        pytest.fail(f"Failed to retrieve zones: {e}")


@pytest.mark.parametrize("client_name, base_url", test_cases)
def test_get_edge_cloud_zones_details(client_name, base_url, zone_id=zone_id):
    """
    Test that get_edge_cloud_zone_details returns valid responses for each client.
    Since each client has different response formats, we only verify basic success criteria.
    """
    edgecloud_platform = EdgeCloudFactory.create_edgecloud_client(client_name, base_url)
    try:
        zones = edgecloud_platform.get_edge_cloud_zones()
        assert len(zones) > 0, "No zones available for testing"

        zone_details = edgecloud_platform.get_edge_cloud_zones_details(zone_id)

        # Basic checks that apply to all clients
        assert zone_details is not None, "Zone details should not be None"
        assert isinstance(zone_details, dict), "Zone details should be a dictionary"
        assert len(zone_details) > 0, "Zone details should not be empty"

    except EdgeCloudPlatformError as e:
        pytest.fail(f"Failed to retrieve zone details: {e}")
    except KeyError as e:
        pytest.fail(f"Missing expected key in response: {e}")
