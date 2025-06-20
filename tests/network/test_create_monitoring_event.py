

import pytest

from sunrise6g_opensdk.common.sdk import Sdk as sdkclient
from sunrise6g_opensdk.network.core.common import CoreHttpError
from sunrise6g_opensdk.network.core.network_interface import NetworkManagementInterface
from sunrise6g_opensdk.network.core.schemas import RetrievalLocationRequest


from tests.network.conftest import instantiate_network_client, camara_payload_input_data


def test_camara_tf_3gpp_event(network_client : NetworkManagementInterface ,camara_payload_input_data: RetrievalLocationRequest, expected_output_data) -> None:
    actual_result = network_client._build_monitoring_event_subscription(retrieve_location_request=camara_payload_input_data)
    assert actual_result == expected_output_data


# def test_create_monitoring_event():