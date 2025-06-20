import pytest

from sunrise6g_opensdk.common.sdk import Sdk as sdkclient
from sunrise6g_opensdk.network.core.schemas import RetrievalLocationRequest, Device, MonitoringEventSubscriptionRequest




@pytest.fixture(scope="session", name="network_client")
def instantiate_network_client():
    """Fixture to create and share a network client across tests"""
    client_specs = {
        "network": {
            "client_name": "open5gs",
            "base_url": "http://127.0.0.1:8082/",
            "scs_as_id": "af_1",
        }
    }
    clients = sdkclient.create_clients_from(client_specs)
    return clients.get("network")


# Test full input data from Camara Payload
# {
#   "phoneNumber": "+1234567890",
#   "networkAccessIdentifier": "user123@example.com",
#   "ipv4Address": {
#     "publicAddress": "198.51.100.10",
#     "privateAddress": "10.0.0.1",
#     "publicPort": 12345
#   },
#   "ipv6Address": "2001:0db8:85a3:0000:0000:8a2e:0370:7334"
# }

@pytest.fixture(scope="module")
def camara_payload_input_data() -> RetrievalLocationRequest:
    """
    Fixture to provide input data for CAMARA payload.
    This data is used in tests that require a specific payload structure.
    """

    return RetrievalLocationRequest(device=Device(phoneNumber="+1234567890"))

# Sample output test data 3GPP MonitoringEventSubscription Request Payload
# {
#   "msisdn": "+306912345678",
#   "notificationDestination": "https://af.example.com/location_notifications",
#   "monitoringType": "LOCATION_REPORTING",
#   "locationType": "CURRENT_LOCATION"
# }
@pytest.fixture(scope="module", name="expected_output_data")
def monitoring_request_3gpp_payload_output_data(camara_payload_input_data: RetrievalLocationRequest) -> MonitoringEventSubscriptionRequest:
    """
    Fixture to provide output data for 3GPP monitoring event request payload.
    """
    output_msisdn = camara_payload_input_data.device.phoneNumber.root.lstrip('+')
    return MonitoringEventSubscriptionRequest(
        msisdn=output_msisdn,
        notificationDestination="http://127.0.0.1:8001",
        monitoringType="LOCATION_REPORTING",
        locationType="LAST_KNOWN_LOCATION"
    )