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
    # Map client names to their corresponding client classes
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
    # Create the edgecloud client
    edgecloud_platform = EdgeCloudFactory.create_edgecloud_client(
        client_name, base_url
    )

    # Case 1: status & region (which are optional) not specified
    zones = edgecloud_platform.get_edge_cloud_zones()
    assert isinstance(
        zones, list
    ), f"Expected a list of zones for {client_name}, but got {type(zones)}"
    if zones:  # Check content if the list is not empty
        assert all(
            isinstance(zone, dict) for zone in zones
        ), "Each zone should be a dictionary"

    # Case 2: region specified
    zones = edgecloud_platform.get_edge_cloud_zones(region="Omega")
    assert isinstance(
        zones, dict
    ), (
        (
            f"Expected a dict for {client_name} when region is specified, "
            f"but got {type(zones)}"
        )
    )

    # Case 3: status specified
    zones = edgecloud_platform.get_edge_cloud_zones(status="active")
    assert isinstance(
        zones, list
    ), f"Expected a list of zones for {client_name}, but got {type(zones)}"
    if zones:  # Check content if the list is not empty
        assert all(
            isinstance(zone, dict) for zone in zones
        ), "Each zone should be a dictionary"

    # Case 4: status & region specified
    zones = edgecloud_platform.get_edge_cloud_zones(
        region="Omega", status="active"
    )
    assert isinstance(
        zones, dict
    ), (
        f"Expected a dict for {client_name} when region & status is specified, "
        f"but got {type(zones)}"
    )


#######################################
# ARTIFACT MANAGEMENT (only for i2Edge)
#######################################
artefact_id = "hello-world-from-sdk"


@pytest.mark.parametrize("client_name, base_url", test_cases)
def test_create_artefact_success(client_name, base_url):
    if client_name == "i2edge":
        edgecloud_platform = EdgeCloudFactory.create_edgecloud_client(
            client_name, base_url
        )

        try:
            edgecloud_platform._create_artefact(
                artefact_id=artefact_id,
                artefact_name="hello-world",
                repo_name="dummy-repo",
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
                artefact_name="test-artefact",
                repo_name="test-repo",
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
# TODO


#######################################
# APP MANAGEMENT
#######################################
# TODO
