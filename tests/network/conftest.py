import pytest

from sunrise6g_opensdk.common.sdk import Sdk as sdkclient
from sunrise6g_opensdk.network.core.schemas import RetrievalLocationRequest, Device, MonitoringEventSubscriptionRequest, Location, AreaType, PointList, Point,Polygon




@pytest.fixture(scope="session", name="network_client")
def instantiate_network_client():
    """Fixture to create and share a network client across tests"""
    client_specs = {
        "network": {
            "client_name": "open5gs",
            "base_url": "http://127.0.0.1:8000/",
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

    return RetrievalLocationRequest(device=Device(phoneNumber="+306912345678"))

# Sample output test data 3GPP MonitoringEventSubscription Request Payload
# {
#   "msisdn": "+306912345678",
#   "notificationDestination": "https://af.example.com/location_notifications",
#   "monitoringType": "LOCATION_REPORTING",
#   "locationType": "CURRENT_LOCATION"
# }
@pytest.fixture(scope="module", name="expected_3gpp_output_data")
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


@pytest.fixture(scope="module", name="expected_camara_output_data")
def monitoring_request_camara_payload_output_data(camara_payload_input_data: RetrievalLocationRequest) -> Location:
    """
    Fixture to provide output data for 3GPP monitoring event request payload.

    Example:

    {
        "lastLocationTime": "2025-06-23T20:47:22Z",
        "area": {
            "areaType": "POLYGON",
            "boundary": [
            {
                "latitude": 37.9838,
                "longitude": 23.7275
            },
            {
                "latitude": 37.98,
                "longitude": 23.75
            },
            {
                "latitude": 37.97,
                "longitude": 23.73
            },
            {   "latitude": 37.975,
                "longtitude": 23.71
            }
            ]
        }
    }
    """
    point1 = Point(latitude=37.9838, longitude=23.7275)
    point2 = Point(latitude=37.98, longitude=23.75)
    point3 = Point(latitude=37.97, longitude=23.73)
    point4 = Point(latitude=37.975, longitude=23.71)

    point_list = PointList(root=[point1, point2, point3,point4])
    
    polygon_area = Polygon(areaType=AreaType.polygon,boundary=point_list)

    location = Location(lastLocationTime="2025-06-23T20:47:22Z",area=polygon_area)
    return location
