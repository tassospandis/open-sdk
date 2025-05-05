# -*- coding: utf-8 -*-
from itertools import product
from typing import Dict

from pydantic import ValidationError
from src import logger
from src.network.core.network_interface import NetworkManagementInterface
from . import common
from . import schemas

log = logger.get_logger(__name__)

flow_id_mapping = {
    "qos-e": 3,
    "qos-s": 4,
    "qos-m": 5,
    "qos-l": 6
}

def flatten_port_spec(ports_spec: schemas.PortsSpec | None)-> list[str]:
    has_ports = False
    has_ranges = False
    flat_ports = []
    if ports_spec and ports_spec.ports:
        has_ports = True
        flat_ports.extend([str(port) for port in ports_spec.ports])
    if ports_spec and ports_spec.ranges:
        has_ranges = True
        flat_ports.extend([f"{range.from_}-{range.to}" for range in ports_spec.ranges])
    if not has_ports and not has_ranges:
        flat_ports.append("0-65535")
    return flat_ports

class NetworkManager(NetworkManagementInterface):
    """
    This client implements the NetworkManagementInterface and translates the
    CAMARA APIs into specific HTTP requests understandable by the Open5GS NEF API.

    Invloved partners and their roles in this implementation:
    - I2CAT: Responsible for the CAMARA QoD API and its mapping to the
             3GPP AsSessionWithQoS API exposed by Open5GS NEF.
    - NCSRD: Responsible for the CAMARA Location API and its mapping to the
             3GPP Monitoring Event API exposed Open5GS NEF.
    """

    def __init__(self, base_url: str, scs_as_id: str):
        """
        Initializes the Open5GS Client.
        """
        try:
            self.base_url = base_url
            self.scs_as_id = scs_as_id
            log.info(
                f"Initialized Open5GSClient with base_url: {self.base_url} "
                f"and scs_as_id: {self.scs_as_id}"
            )
        except Exception as e:
            log.error(f"Failed to initialize Open5GSClient: {e}")
            raise e

    # --- Implementation of NetworkManagementInterface methods ---
    def create_qod_session(self, session_info: Dict) -> Dict:
        """
        Creates a QoD session based on the CAMARA QoD API input.
        Maps the CAMARA QoD POST /sessions to Open5GS NEF POST /{scsAsId}/subscriptions.
        """
        url = f"{self.base_url}/{self.scs_as_id}/subscriptions"
        # Raises ValidationError if the object is not valid.
        valid_session_info = schemas.CreateSession.model_validate(session_info)
        if valid_session_info.qosProfile not in flow_id_mapping.keys():
            raise ValidationError(f"Open5Gs only supports these qos-profiles: {", ".join(flow_id_mapping.keys())}")

        flow_id = flow_id_mapping[valid_session_info.qosProfile]
        device_ip = valid_session_info.device.ipv4Address or session_info.device.ipv4Address
        server_ip = valid_session_info.applicationServer.ipv4Address or valid_session_info.applicationServer.ipv6Address
        device_ports = flatten_port_spec(valid_session_info.devicePorts)
        server_ports = flatten_port_spec(valid_session_info.applicationServerPorts)
        ports_combis = list(product(device_ports, server_ports))

        flow_descrs = []
        for device_port, server_port in ports_combis:
            flow_descrs.append(f"permit in ip from {device_ip} {device_port} to {server_ip} {server_port}")
            flow_descrs.append(f"permit out ip from {device_ip} {device_port} to {server_ip} {server_port}")
        flows = [schemas.FlowInfo(
            flowId=flow_id,
            flowDescriptions=[", ".join(flow_descrs)]
        )]
        subscription = schemas.AsSessionWithQoSSubscription(
            supportedFeatures=schemas.SupportedFeatures("003C"),
            flowInfo=flows,
            qosReference = valid_session_info.qosProfile,
            ueIpv4Addr=valid_session_info.device.ipv4Address,
            ueIpv6Addr=valid_session_info.device.ipv6Address,
        )
        common.open5gs_post(url, subscription)

    def get_qod_session(self, session_id: str) -> Dict:
        """
        Retrieves a specific Open5GS QoS Subscription details.
        Maps CAMARA QoD GET /sessions/{sessionId} to Open5GS NEF GET /
        {scsAsId}/subscriptions/{subscriptionId}.
        """
        url = f"{self.base_url}/{self.scs_as_id}/subscriptions/{session_id}"
        common.open5gs_get(url)

    def delete_qod_session(self, session_id: str) -> None:
        """
        Deletes a specific Open5GS QoS Subscription.
        Maps CAMARA QoD DELETE /sessions/{sessionId} to Open5GS NEF DELETE /
        {scsAsId}/subscriptions/{subscriptionId}.
        """
        url = f"{self.base_url}/{self.scs_as_id}/subscriptions/{session_id}"
        common.open5gs_delete(url)

# Note:
# As this class is inheriting from NetworkManagementInterface, it is
# expected to implement all the abstract methods defined in that interface.
#
# In case this network adapter doesn't support a specific method, it should
# be marked as NotImplementedError.
