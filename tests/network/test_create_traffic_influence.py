# # -*- coding: utf-8 -*-
import time

import pytest

from sunrise6g_opensdk.common.sdk import Sdk as sdkclient
from sunrise6g_opensdk.network.core.common import CoreHttpError
from sunrise6g_opensdk.network.core.network_interface import NetworkManagementInterface
from tests.network.test_cases import test_cases


@pytest.fixture(scope="module", name="network_client")
def instantiate_network_client(request):
    """Fixture to create and share a network client across tests"""
    client_specs = request.param
    clients = sdkclient.create_clients_from(client_specs)
    return clients.get("network")


def id_func(val):
    return val["network"]["client_name"]


@pytest.mark.parametrize(
    "network_client",
    test_cases,
    ids=id_func,
    indirect=True,
)
def test_valid_input(network_client: NetworkManagementInterface):

    ti_session = {
        "device": {
            "ipv4Address": {"publicAddress": "12.1.2.31", "privateAddress": "12.1.2.31"}
        },
        "edgeCloudZoneId": "edge",
        "appId": "testSdk-ffff-aaaa-c0ffe",
        "appInstanceId": "172.21.18.3",
        "notificationUri": "https://endpoint.example.com/sink",
    }
    network_client._build_ti_subscription(ti_session)


@pytest.fixture(scope="module")
def traffic_influence_id(network_client: NetworkManagementInterface):

    ti_session = {
        "device": {
            "ipv4Address": {"publicAddress": "12.1.2.31", "privateAddress": "12.1.2.31"}
        },
        "edgeCloudZoneId": "edge",
        "appId": "testSdk-ffff-aaaa-c0ffe",
        "appInstanceId": "172.21.18.3",
        "notificationUri": "https://endpoint.example.com/sink",
    }
    try:
        response = network_client.create_traffic_influence_resource(ti_session)
        assert response is not None, "Response should not be None"
        assert isinstance(response, dict), "Response should be a dictionary"
        assert (
            "trafficInfluenceID" in response
        ), "Response should contain 'trafficInfluenceID'"
        yield str(response["trafficInfluenceID"])
    finally:
        pass


@pytest.mark.parametrize(
    "network_client",
    test_cases,
    ids=id_func,
    indirect=True,
)
def test_create_traffic_influence(traffic_influence_id):
    assert traffic_influence_id is not None


@pytest.mark.parametrize("network_client", test_cases, ids=id_func, indirect=True)
def test_timer_wait_5_seconds(network_client):
    time.sleep(5)


@pytest.mark.parametrize("network_client", test_cases, ids=id_func, indirect=True)
def test_put_traffic_influence_session(
    network_client: NetworkManagementInterface, traffic_influence_id
):
    try:
        ti_session = {
            "device": {
                "ipv4Address": {
                    "publicAddress": "12.1.2.31",
                    "privateAddress": "12.1.2.31",
                }
            },
            "edgeCloudZoneId": "edge",
            "appId": "testSdk-ffff-aaaa-c0ffe",
            "appInstanceId": "172.21.18.5",
            "notificationUri": "https://endpoint.example.com/sink",
        }
        network_client.put_traffic_influence_resource(traffic_influence_id, ti_session)
    except CoreHttpError as e:
        pytest.fail(f"Failed to update traffic influence session: {e}")


@pytest.mark.parametrize("network_client", test_cases, ids=id_func, indirect=True)
def test_delete_traffic_influence_session(
    network_client: NetworkManagementInterface, traffic_influence_id
):
    try:
        network_client.delete_traffic_influence_resource(traffic_influence_id)
    except CoreHttpError as e:
        pytest.fail(f"Failed to delete traffic influence: {e}")
