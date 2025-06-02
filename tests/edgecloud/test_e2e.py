# -*- coding: utf-8 -*-
"""
EdgeCloud Platform Integration Tests

Validates the complete application lifecycle across multiple clients:
1. Infrastructure (zone discovery)
2. Artefact management (create/delete)
3. Application lifecycle (onboard/deploy/undeploy/delete)

Key features:
- Tests all client implementations (parametrized via test_cases)
- Ensures proper resource cleanup
- Uses shared test constants and CAMARA-compliant manifests
- Includes i2edge-specific tests where needed
"""
import pytest

from src.edgecloud.clients.errors import EdgeCloudPlatformError
from src.edgecloud.core.edgecloud_factory import EdgeCloudFactory
from tests.edgecloud.test_cases import test_cases
from tests.edgecloud.test_config import (
    APP_ID,
    APP_ONBOARD_MANIFEST,
    APP_ZONES,
    ARTEFACT_ID,
    ARTEFACT_NAME,
    REPO_NAME,
    REPO_TYPE,
    REPO_URL,
    ZONE_ID,
)


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
def test_get_edge_cloud_zones_details(client_name, base_url, zone_id=ZONE_ID):
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


@pytest.mark.parametrize("client_name, base_url", test_cases)
def test_create_artefact_success(client_name, base_url):
    if client_name == "i2edge":
        edgecloud_platform = EdgeCloudFactory.create_edgecloud_client(
            client_name, base_url
        )
        try:
            edgecloud_platform._create_artefact(
                artefact_id=ARTEFACT_ID,
                artefact_name=ARTEFACT_NAME,
                repo_name=REPO_NAME,
                repo_type=REPO_TYPE,
                repo_url=REPO_URL,
                password=None,
                token=None,
                user_name=None,
            )
        except EdgeCloudPlatformError as e:
            pytest.fail(f"Artefact creation failed unexpectedly: {e}")


@pytest.mark.parametrize("client_name, base_url", test_cases)
def test_onboard_app_success(client_name, base_url):
    edgecloud_platform = EdgeCloudFactory.create_edgecloud_client(client_name, base_url)
    try:
        edgecloud_platform.onboard_app(APP_ONBOARD_MANIFEST)
    except EdgeCloudPlatformError as e:
        pytest.fail(f"App onboarding failed unexpectedly: {e}")


@pytest.fixture(scope="module")
def deployed_app(request):
    client_name, base_url = request.param
    edgecloud_platform = EdgeCloudFactory.create_edgecloud_client(client_name, base_url)
    try:
        output = edgecloud_platform.deploy_app(APP_ID, APP_ZONES)
        return {
            "client_name": client_name,
            "base_url": base_url,
            "appInstanceId": output["deploy_name"],
        }
    except EdgeCloudPlatformError as e:
        pytest.fail(f"App deployment failed unexpectedly: {e}")


@pytest.mark.parametrize("deployed_app", test_cases, indirect=True)
def test_deploy_app_success(deployed_app):
    assert "appInstanceId" in deployed_app
    if "client_name" in deployed_app == "i2edge":
        assert deployed_app["appInstanceId"].startswith(ARTEFACT_NAME)


@pytest.mark.parametrize("deployed_app", test_cases, indirect=True)
def test_undeploy_app_success(deployed_app):
    edgecloud_platform = EdgeCloudFactory.create_edgecloud_client(
        deployed_app["client_name"], deployed_app["base_url"]
    )
    try:
        edgecloud_platform.undeploy_app(deployed_app["appInstanceId"])
    except EdgeCloudPlatformError as e:
        pytest.fail(f"App undeployment failed unexpectedly: {e}")


@pytest.mark.parametrize("client_name, base_url", test_cases)
def test_delete_onboarded_app_success(client_name, base_url):
    edgecloud_platform = EdgeCloudFactory.create_edgecloud_client(client_name, base_url)
    try:
        edgecloud_platform.delete_onboarded_app(app_id=APP_ONBOARD_MANIFEST["appId"])
    except EdgeCloudPlatformError as e:
        pytest.fail(f"App onboarding deletion failed unexpectedly: {e}")


@pytest.mark.parametrize("client_name, base_url", test_cases)
def test_delete_artefact_success(client_name, base_url):
    if client_name == "i2edge":
        edgecloud_platform = EdgeCloudFactory.create_edgecloud_client(
            client_name, base_url
        )
        try:
            edgecloud_platform._delete_artefact(artefact_id=ARTEFACT_ID)
        except EdgeCloudPlatformError as e:
            pytest.fail(f"Artefact deletion failed unexpectedly: {e}")
