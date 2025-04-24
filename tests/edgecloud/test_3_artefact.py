# -*- coding: utf-8 -*-
import pytest

from src.edgecloud.clients.errors import EdgeCloudPlatformError
from src.edgecloud.core.edgecloud_factory import EdgeCloudFactory

# Note: artifact mgmt is only supported by i2Edge

test_cases = [
    ("i2edge", "http://192.168.123.237:30769/"),
]

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
                user_name=None,
            )
        except EdgeCloudPlatformError as e:
            pytest.fail(f"Artefact creation failed unexpectedly: {e}")


@pytest.mark.parametrize("client_name, base_url", test_cases)
def test_create_artefact_failure(client_name, base_url):
    if client_name == "i2edge":
        edgecloud_platform = EdgeCloudFactory.create_edgecloud_client(
            client_name, base_url
        )
        with pytest.raises(EdgeCloudPlatformError):
            edgecloud_platform._create_artefact(
                artefact_id=artefact_id,
                artefact_name=artefact_name,
                repo_name=repo_name,
                repo_type="PUBLICREPO",
                repo_url="http://invalid.url",
                password=None,
                token=None,
                user_name=None,
            )


@pytest.mark.parametrize("client_name, base_url", test_cases)
def test_get_artefact_success(client_name, base_url):
    edgecloud_platform = EdgeCloudFactory.create_edgecloud_client(client_name, base_url)
    try:
        edgecloud_platform._get_artefact(artefact_id=artefact_id)
    except EdgeCloudPlatformError as e:
        pytest.fail(f"Artefact retrieval failed unexpectedly: {e}")


@pytest.mark.parametrize("client_name, base_url", test_cases)
def test_get_artefact_failure(client_name, base_url):
    edgecloud_platform = EdgeCloudFactory.create_edgecloud_client(client_name, base_url)
    with pytest.raises(EdgeCloudPlatformError):
        edgecloud_platform._get_artefact(artefact_id="non-existent-artefact")


@pytest.mark.parametrize("client_name, base_url", test_cases)
def test_get_all_artefacts_success(client_name, base_url):
    edgecloud_platform = EdgeCloudFactory.create_edgecloud_client(client_name, base_url)
    try:
        edgecloud_platform._get_all_artefacts()
    except EdgeCloudPlatformError as e:
        pytest.fail(f"Artefact retrieval failed unexpectedly: {e}")


@pytest.mark.parametrize("client_name, base_url", test_cases)
def test_delete_artefact_success(client_name, base_url):
    edgecloud_platform = EdgeCloudFactory.create_edgecloud_client(client_name, base_url)
    try:
        edgecloud_platform._delete_artefact(artefact_id=artefact_id)
    except EdgeCloudPlatformError as e:
        pytest.fail(f"Artefact deletion failed unexpectedly: {e}")


@pytest.mark.parametrize("client_name, base_url", test_cases)
def test_delete_artefact_failure(client_name, base_url):
    edgecloud_platform = EdgeCloudFactory.create_edgecloud_client(client_name, base_url)
    with pytest.raises(EdgeCloudPlatformError):
        edgecloud_platform._delete_artefact(artefact_id="non-existent-artefact")
