# -*- coding: utf-8 -*-
import pytest

from src.edgecloud.clients.errors import EdgeCloudPlatformError
from src.edgecloud.core.edgecloud_factory import EdgeCloudFactory
from tests.edgecloud.test_cases import test_cases

# CAMARA app payload (only mandatory fields)
app_manifest = {
    "appId": "test_app_from_SDK",
    "name": "my-application",
    "version": "1.0.0",
    "appProvider": "MyAppProvider",
    "packageType": "CONTAINER",
    "appRepo": {
        "type": "PUBLICREPO",
        "imagePath": "https://example.com/my-app-image:1.0.0",
    },
    "requiredResources": {
        "infraKind": "kubernetes",
        "applicationResources": {
            "cpuPool": {
                "numCPU": 2,
                "memory": 2048,
                "topology": {
                    "minNumberOfNodes": 2,
                    "minNodeCpu": 1,
                    "minNodeMemory": 1024,
                },
            }
        },
        "isStandalone": False,
        "version": "1.29",
    },
    "componentSpec": [
        {
            "componentName": "my-component",
            "networkInterfaces": [
                {
                    "interfaceId": "eth0",
                    "protocol": "TCP",
                    "port": 8080,
                    "visibilityType": "VISIBILITY_EXTERNAL",
                }
            ],
        }
    ],
}


@pytest.mark.parametrize("client_name, base_url", test_cases)
def test_onboard_app_success(client_name, base_url):
    edgecloud_platform = EdgeCloudFactory.create_edgecloud_client(client_name, base_url)
    try:
        edgecloud_platform.onboard_app(app_manifest)
    except EdgeCloudPlatformError as e:
        pytest.fail(f"App onboarding failed unexpectedly: {e}")


@pytest.mark.parametrize("client_name, base_url", test_cases)
def test_onboard_app_failure(client_name, base_url):
    edgecloud_platform = EdgeCloudFactory.create_edgecloud_client(client_name, base_url)
    with pytest.raises(EdgeCloudPlatformError):
        edgecloud_platform.onboard_app({})


@pytest.mark.parametrize("client_name, base_url", test_cases)
def test_get_onboarded_app_success(client_name, base_url):
    edgecloud_platform = EdgeCloudFactory.create_edgecloud_client(client_name, base_url)
    try:
        edgecloud_platform.get_onboarded_app(app_id=app_manifest["appId"])
    except EdgeCloudPlatformError as e:
        pytest.fail(f"App onboarding failed unexpectedly: {e}")


@pytest.mark.parametrize("client_name, base_url", test_cases)
def test_get_onboarded_app_failure(client_name, base_url):
    edgecloud_platform = EdgeCloudFactory.create_edgecloud_client(client_name, base_url)
    with pytest.raises(EdgeCloudPlatformError):
        edgecloud_platform.get_onboarded_app(app_id="non-existent-app")


@pytest.mark.parametrize("client_name, base_url", test_cases)
def test_get_all_onboarded_app_success(client_name, base_url):
    edgecloud_platform = EdgeCloudFactory.create_edgecloud_client(client_name, base_url)
    try:
        edgecloud_platform.get_all_onboarded_apps()
    except EdgeCloudPlatformError as e:
        pytest.fail(f"App onboarding failed unexpectedly: {e}")


@pytest.mark.parametrize("client_name, base_url", test_cases)
def test_delete_onboarded_app_success(client_name, base_url):
    edgecloud_platform = EdgeCloudFactory.create_edgecloud_client(client_name, base_url)
    try:
        edgecloud_platform.delete_onboarded_app(app_id=app_manifest["appId"])
    except EdgeCloudPlatformError as e:
        pytest.fail(f"App onboarding deletion failed unexpectedly: {e}")


@pytest.mark.parametrize("client_name, base_url", test_cases)
def test_delete_onboarded_app_failure(client_name, base_url):
    edgecloud_platform = EdgeCloudFactory.create_edgecloud_client(client_name, base_url)
    with pytest.raises(EdgeCloudPlatformError):
        edgecloud_platform.delete_onboarded_app(app_id="non-existent-app")
