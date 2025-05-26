# -*- coding: utf-8 -*-
from typing import Dict

from pydantic import ValidationError
from src import logger
from src.network.core.network_interface import NetworkManagementInterface, build_flows
from ...core import common
from ...core import schemas

log = logger.get_logger(__name__)

flow_id_mapping = {"qos-e": 3, "qos-s": 4, "qos-m": 5, "qos-l": 6}


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

    def core_specific_validation(self, session_info: schemas.CreateSession):
        if session_info.qosProfile not in flow_id_mapping.keys():
            raise ValidationError(
                f"Open5Gs only supports these qos-profiles: {', '.join(flow_id_mapping.keys())}"
            )

    def add_core_specific_parameters(
        self, session_info: schemas.AsSessionWithQoSSubscription
    ) -> None:
        session_info.supportedFeatures = schemas.SupportedFeatures("003C")
        flow_id = flow_id_mapping[session_info.qosProfile]
        session_info.flowInfo = build_flows(flow_id, session_info)

    # --- Implementation of NetworkManagementInterface methods ---
    def create_qod_session(self, session_info: Dict) -> Dict:
        """
        Creates a QoD session based on the CAMARA QoD API input.
        Maps the CAMARA QoD POST /sessions to Open5GS NEF POST /{scsAsId}/subscriptions.
        """
        url = f"{self.base_url}/{self.scs_as_id}/subscriptions"
        # Raises ValidationError if the object is not valid.
        valid_session_info = schemas.CreateSession.model_validate(session_info)

        subscription = schemas.AsSessionWithQoSSubscription(
            notificationDestination=valid_session_info.sink,
            qosReference=valid_session_info.qosProfile,
            ueIpv4Addr=valid_session_info.device.ipv4Address,
            ueIpv6Addr=valid_session_info.device.ipv6Address,
            usageThreshold=schemas.UsageThreshold(duration=valid_session_info.duration),
        )
        self.add_core_specific_parameters(subscription)
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
