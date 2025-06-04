# -*- coding: utf-8 -*-
import pytest

from src.common.sdk_catalog_client import SdkCatalogClient

OPEN5GS_TEST_CASES = [
    {
        "network": {
            "client_name": "open5gs",
            "base_url": "http://192.168.124.233:30769/",
            "scs_as_id": "scs1",
        }
    }
]


@pytest.mark.parametrize(
    "client_specs",
    OPEN5GS_TEST_CASES,
    ids=["open5gs"],
)
def test_valid_input_open5gs(client_specs):
    network_client = SdkCatalogClient.create_clients_from(client_specs)["network"]

    camara_session = {
        "duration": 3600,
        "device": {
            "ipv4Address": {"publicAddress": "10.45.0.3", "privateAddress": "10.45.0.3"}
        },
        "applicationServer": {"ipv4Address": "10.45.0.1"},
        "devicePorts": {"ranges": [{"from": 0, "to": 65535}]},
        "applicationServerPorts": {"ranges": [{"from": 0, "to": 65535}]},
        "qosProfile": "qos-e",
        "sink": "https://endpoint.example.com/sink",
    }
    network_client._build_qod_subscription(camara_session)


@pytest.mark.parametrize(
    "client_specs",
    OPEN5GS_TEST_CASES,
    ids=["open5gs"],
)
def test_create_qod_session_open5gs(client_specs):
    network_client = SdkCatalogClient.create_clients_from(client_specs)["network"]

    camara_session = {
        "duration": 3600,
        "device": {
            "ipv4Address": {"publicAddress": "10.45.0.3", "privateAddress": "10.45.0.3"}
        },
        "applicationServer": {"ipv4Address": "10.45.0.1"},
        "devicePorts": {"ranges": [{"from": 0, "to": 65535}]},
        "applicationServerPorts": {"ranges": [{"from": 0, "to": 65535}]},
        "qosProfile": "qos-e",
        "sink": "https://endpoint.example.com/sink",
    }
    network_client.create_qod_session(camara_session)
