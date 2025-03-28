import pytest

from src.edgecloud.clients.aeros.client import EdgeApplicationManager as AerosClient
from src.edgecloud.clients.dmo.client import EdgeApplicationManager as DmoClient
from src.edgecloud.clients.i2edge.client import EdgeApplicationManager as I2EdgeClient
from src.edgecloud.clients.i2edge.client import I2EdgeError
from src.edgecloud.clients.piedge.client import EdgeApplicationManager as PiEdgeClient
from src.edgecloud.core.edgecloud_factory import EdgeCloudFactory

# Define common test cases for all tests
test_cases = [
    ("i2edge", "http://192.168.123.237:30769/"),
    # ("aeros", "http://aeros.example.com/"),
    # ("piedge", "http://piedge.example.com/"),
    # ("dmo", "http://dmo.example.com/")
]


#######################################
# EDGECLOUD CLIENT'S INSTANTIATION
#######################################
@pytest.mark.parametrize("client_name, base_url", test_cases)
def test_factory_edgecloud(client_name, base_url):
    """
    Test the factory pattern for the edgecloud client.
    """
    client_class_map = {
        "i2edge": I2EdgeClient,
        "aeros": AerosClient,
        "piedge": PiEdgeClient,
        "dmo": DmoClient,
    }

    expected_client_class = client_class_map[client_name]
    edgecloud_platform = EdgeCloudFactory.create_edgecloud_client(
        client_name, base_url
    )
    assert isinstance(edgecloud_platform, expected_client_class)


#######################################
# GET EDGE CLOUD ZONES
#######################################
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
    except I2EdgeError as e:
        pytest.fail(f"Failed to retrieve zones: {e}")


#######################################
# ARTIFACT MANAGEMENT (only for i2Edge)
#######################################
artefact_id = "hello-world-from-sdk-2"
artefact_name = "hello-word-2"
repo_name = "dummy-repo-2"


@pytest.mark.parametrize("client_name, base_url", test_cases)
def test_create_artefact_success(client_name, base_url):
    if client_name == "i2edge":
        edgecloud_platform = EdgeCloudFactory.create_edgecloud_client(
            client_name, base_url
        )

        try:
            edgecloud_platform._create_artefact(
                artefact_id=artefact_id,
                artefact_name=artefact_name,
                repo_name=repo_name,
                repo_type="PUBLICREPO",
                repo_url="https://helm.github.io/examples",
                password=None,
                token=None,
                user_name=None
            )
        except I2EdgeError as e:
            pytest.fail(f"Artefact creation failed unexpectedly: {e}")


@pytest.mark.parametrize("client_name, base_url", test_cases)
def test_create_artefact_failure(client_name, base_url):
    if client_name == "i2edge":
        edgecloud_platform = EdgeCloudFactory.create_edgecloud_client(
            client_name, base_url
        )

        with pytest.raises(I2EdgeError):
            edgecloud_platform._create_artefact(
                artefact_id=artefact_id,
                artefact_name=artefact_name,
                repo_name=repo_name,
                repo_type="PUBLICREPO",
                repo_url="http://invalid.url",
                password=None,
                token=None,
                user_name=None
            )


@pytest.mark.parametrize("client_name, base_url", test_cases)
def test_get_artefact_success(client_name, base_url):
    if client_name == "i2edge":
        edgecloud_platform = EdgeCloudFactory.create_edgecloud_client(
            client_name, base_url
        )

        try:
            edgecloud_platform._get_artefact(artefact_id=artefact_id)
        except I2EdgeError as e:
            pytest.fail(f"Artefact retrieval failed unexpectedly: {e}")


@pytest.mark.parametrize("client_name, base_url", test_cases)
def test_get_artefact_failure(client_name, base_url):
    if client_name == "i2edge":
        edgecloud_platform = EdgeCloudFactory.create_edgecloud_client(
            client_name, base_url
        )

        with pytest.raises(I2EdgeError):
            edgecloud_platform._get_artefact(artefact_id="non-existent-artefact")


@pytest.mark.parametrize("client_name, base_url", test_cases)
def test_get_all_artefacts_success(client_name, base_url):
    if client_name == "i2edge":
        edgecloud_platform = EdgeCloudFactory.create_edgecloud_client(
            client_name, base_url
        )

        try:
            edgecloud_platform._get_all_artefacts()
        except I2EdgeError as e:
            pytest.fail(f"Artefact retrieval failed unexpectedly: {e}")

@pytest.mark.parametrize("client_name, base_url", test_cases)
def test_delete_artefact_success(client_name, base_url):
    if client_name == "i2edge":
        edgecloud_platform = EdgeCloudFactory.create_edgecloud_client(
            client_name, base_url
        )

        try:
            edgecloud_platform._delete_artefact(artefact_id=artefact_id)
        except I2EdgeError as e:
            pytest.fail(f"Artefact deletion failed unexpectedly: {e}")


@pytest.mark.parametrize("client_name, base_url", test_cases)
def test_delete_artefact_failure(client_name, base_url):
    if client_name == "i2edge":
        edgecloud_platform = EdgeCloudFactory.create_edgecloud_client(
            client_name, base_url
        )

        with pytest.raises(I2EdgeError):
            edgecloud_platform._delete_artefact(artefact_id="non-existent-artefact")


#######################################
# APP ONBOARDING
#######################################
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
# artefactId needs to be added; same ID as appId
app_manifest.update({"artefactId": app_manifest["appId"]})


@pytest.mark.parametrize("client_name, base_url", test_cases)
def test_onboard_app_success(client_name, base_url):
    edgecloud_platform = EdgeCloudFactory.create_edgecloud_client(
        client_name, base_url
    )

    try:
        edgecloud_platform.onboard_app(app_manifest)
    except I2EdgeError as e:
        pytest.fail(f"App onboarding failed unexpectedly: {e}")


@pytest.mark.parametrize("client_name, base_url", test_cases)
def test_onboard_app_failure(client_name, base_url):
    edgecloud_platform = EdgeCloudFactory.create_edgecloud_client(
        client_name, base_url
    )

    with pytest.raises(I2EdgeError):
        edgecloud_platform.onboard_app({})


@pytest.mark.parametrize("client_name, base_url", test_cases)
def test_onboard_app_failure_artefact_id_missing(client_name, base_url):
    app_manifest.pop("artefactId")

    edgecloud_platform = EdgeCloudFactory.create_edgecloud_client(
        client_name, base_url
    )

    with pytest.raises(I2EdgeError):
        edgecloud_platform.onboard_app({})


@pytest.mark.parametrize("client_name, base_url", test_cases)
def test_get_onboarded_app_success(client_name, base_url):
    edgecloud_platform = EdgeCloudFactory.create_edgecloud_client(
        client_name, base_url
    )

    try:
        edgecloud_platform.get_onboarded_app(app_id=app_manifest["appId"])
    except I2EdgeError as e:
        pytest.fail(f"App onboarding failed unexpectedly: {e}")


@pytest.mark.parametrize("client_name, base_url", test_cases)
def test_get_onboarded_app_failure(client_name, base_url):
    edgecloud_platform = EdgeCloudFactory.create_edgecloud_client(
        client_name, base_url
    )

    with pytest.raises(I2EdgeError):
        edgecloud_platform.get_onboarded_app(app_id="non-existent-app")


@pytest.mark.parametrize("client_name, base_url", test_cases)
def test_get_all_onboarded_app_success(client_name, base_url):
    edgecloud_platform = EdgeCloudFactory.create_edgecloud_client(
        client_name, base_url
    )

    try:
        edgecloud_platform.get_all_onboarded_apps()
    except I2EdgeError as e:
        pytest.fail(f"App onboarding failed unexpectedly: {e}")


@pytest.mark.parametrize("client_name, base_url", test_cases)
def test_delete_onboarded_app_success(client_name, base_url):
    edgecloud_platform = EdgeCloudFactory.create_edgecloud_client(
        client_name, base_url
    )

    try:
        edgecloud_platform.delete_onboarded_app(app_id=app_manifest["appId"])
    except I2EdgeError as e:
        pytest.fail(f"App onboarding deletion failed unexpectedly: {e}")


@pytest.mark.parametrize("client_name, base_url", test_cases)
def test_delete_onboarded_app_failure(client_name, base_url):
    edgecloud_platform = EdgeCloudFactory.create_edgecloud_client(
        client_name, base_url
    )

    with pytest.raises(I2EdgeError):
        edgecloud_platform.delete_onboarded_app(app_id="non-existent-app")


#######################################
# APP MANAGEMENT
#######################################
# TODO
