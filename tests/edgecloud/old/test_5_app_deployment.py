# -*- coding: utf-8 -*-
import pytest

from src.edgecloud.clients.errors import EdgeCloudPlatformError
from src.edgecloud.core.edgecloud_factory import EdgeCloudFactory
from tests.edgecloud.test_cases import test_cases

# As a pre-requirement for this test, the app should be already onboarded
appId = "i2edgechart-id"
app_zones = [
    {
        "kubernetesClusterRef": "not-used",
        "EdgeCloudZone": {
            # "edgeCloudZoneId": "Omega",
            "edgeCloudZoneId": "Omega12345",
            "edgeCloudZoneName": "not-used",
            "edgeCloudZoneStatus": "not-used",
            "edgeCloudProvider": "not-used",
            "edgeCloudRegion": "not-used",
        },
    }
]

# TODO: Revise this test, something is wrong. It doesn't fail even though I specify a non-existent av zone

# @pytest.fixture(scope="module")
# def deployed_app(request):
#     client_name, base_url = request.param
#     edgecloud_platform = EdgeCloudFactory.create_edgecloud_client(client_name, base_url)
#     try:
#         output = edgecloud_platform.deploy_app(appId, app_zones)
#         return {
#             "client_name": client_name,
#             "base_url": base_url,
#             "appInstanceId": output["deploy_name"],
#         }
#     except EdgeCloudPlatformError as e:
#         pytest.fail(f"App deployment failed unexpectedly: {e}")


# @pytest.mark.parametrize("deployed_app", test_cases, indirect=True)
# def test_deploy_app_success(deployed_app):
#     assert "appInstanceId" in deployed_app
#     assert deployed_app["appInstanceId"].startswith("i2edgechart")


@pytest.mark.parametrize("client_name, base_url", test_cases)
def test_get_all_apps_success(client_name, base_url):
    edgecloud_platform = EdgeCloudFactory.create_edgecloud_client(client_name, base_url)
    try:
        edgecloud_platform.get_all_deployed_apps()

    except EdgeCloudPlatformError as e:
        pytest.fail(f"App instance retrieval failed unexpectedly: {e}")


@pytest.mark.parametrize("client_name, base_url", test_cases)
def test_get_app_success(client_name, base_url):
    edgecloud_platform = EdgeCloudFactory.create_edgecloud_client(client_name, base_url)
    try:
        edgecloud_platform.get_deployed_app(
            appId, app_zones[0]["EdgeCloudZone"]["edgeCloudZoneId"]
        )

    except EdgeCloudPlatformError as e:
        pytest.fail(f"App instance retrieval failed unexpectedly: {e}")


# @pytest.mark.parametrize("deployed_app", test_cases, indirect=True)
# def test_undeploy_app_success(deployed_app):
#     edgecloud_platform = EdgeCloudFactory.create_edgecloud_client(
#         deployed_app["client_name"], deployed_app["base_url"]
#     )
#     try:
#         edgecloud_platform.undeploy_app(deployed_app["appInstanceId"])
#     except EdgeCloudPlatformError as e:
#         pytest.fail(f"App undeployment failed unexpectedly: {e}")
