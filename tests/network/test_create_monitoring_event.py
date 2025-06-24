

import pytest

from sunrise6g_opensdk.common.sdk import Sdk as sdkclient
from sunrise6g_opensdk.network.core.common import CoreHttpError
from sunrise6g_opensdk.network.core.network_interface import NetworkManagementInterface
from sunrise6g_opensdk.network.core.schemas import RetrievalLocationRequest, MonitoringEventSubscriptionRequest, Location


from tests.network.conftest import instantiate_network_client, camara_payload_input_data


def test_camara_tf_3gpp_event(network_client : NetworkManagementInterface ,camara_payload_input_data: RetrievalLocationRequest, expected_3gpp_output_data: MonitoringEventSubscriptionRequest) -> None:
    actual_result = network_client._build_monitoring_event_subscription(retrieve_location_request=camara_payload_input_data)
    assert actual_result == expected_3gpp_output_data, f"Expected actual_result ({actual_result}) \n to be equal to expected_result ({expected_3gpp_output_data}), but they were not."
   
def test_create_monitoring_event(network_client : NetworkManagementInterface, camara_payload_input_data: RetrievalLocationRequest,expected_camara_output_data: Location ):
    try:
        actual_result = network_client.create_monitoring_event_subscription(retrieve_location_request=camara_payload_input_data)
        assert actual_result == expected_camara_output_data, f"Expected actual_result ({actual_result}) \n to be equal to expected_result ({expected_camara_output_data}), but they were not."
    except CoreHttpError as e:
        pytest.fail(f"Failed to retrieve event report: {e}")