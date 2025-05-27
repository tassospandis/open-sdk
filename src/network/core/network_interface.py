#!/usr/bin/env python3
# -*- coding: utf-8 -*-
##
# Copyright 2025-present by Software Networks Area, i2CAT.
# All rights reserved.
#
# This file is part of the Open SDK
#
# Contributors:
#   - Reza Mosahebfard (reza.mosahebfard@i2cat.net)
##
from abc import ABC, abstractmethod
from itertools import product
from typing import Dict

from src import logger
from src.network.core import common, schemas

log = logger.get_logger(__name__)


def flatten_port_spec(ports_spec: schemas.PortsSpec | None) -> list[str]:
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


def build_flows(
    flow_id: int,
    session_info: schemas.CreateSession,
) -> list[schemas.FlowInfo]:
    device_ports = flatten_port_spec(session_info.devicePorts)
    server_ports = flatten_port_spec(session_info.applicationServerPorts)
    ports_combis = list(product(device_ports, server_ports))

    device_ip = session_info.device.ipv4Address or session_info.device.ipv4Address
    server_ip = (
        session_info.applicationServer.ipv4Address
        or session_info.applicationServer.ipv6Address
    )

    flow_descrs = []
    for device_port, server_port in ports_combis:
        flow_descrs.append(
            f"permit in ip from {device_ip} {device_port} to {server_ip} {server_port}"
        )
        flow_descrs.append(
            f"permit out ip from {device_ip} {device_port} to {server_ip} {server_port}"
        )
    flows = [
        schemas.FlowInfo(flowId=flow_id, flowDescriptions=[", ".join(flow_descrs)])
    ]
    return flows


class NetworkManagementInterface(ABC):
    """
    Abstract Base Class for Network Resource Management.

    This interface defines the standard methods that all
    Network Clients (Open5GS, OAI, Open5GCore) must implement.

    Partners implementing a new network client should inherit from this class
    and provide concrete implementations for all abstract methods relevant
    to their specific NEF capabilities.
    """

    base_url: str
    scs_as_id: str

    @abstractmethod
    def add_core_specific_parameters(
        self,
        session_info: schemas.CreateSession,
        subscription: schemas.AsSessionWithQoSSubscription,
    ):
        """
        Placeholder for adding core-specific parameters to the subscription.
        This method should be overridden by subclasses to implement specific logic.
        """
        pass

    @abstractmethod
    def core_specific_validation(self, session_info: schemas.CreateSession) -> None:
        """
        Validates core-specific parameters for the session creation.

        args:
            session_info: The session information to validate.

        raises:
            ValidationError: If the session information does not meet core-specific requirements.
        """
        # Placeholder for core-specific validation logic
        # This method should be overridden by subclasses if needed
        pass

    def _build_subscription(self, session_info: Dict) -> None:
        valid_session_info = schemas.CreateSession.model_validate(session_info)
        device_ipv4 = None
        if valid_session_info.device.ipv4Address:
            device_ipv4 = valid_session_info.device.ipv4Address.root.publicAddress.root

        self.core_specific_validation(valid_session_info)
        subscription = schemas.AsSessionWithQoSSubscription(
            notificationDestination=str(valid_session_info.sink),
            qosReference=valid_session_info.qosProfile.root,
            ueIpv4Addr=device_ipv4,
            ueIpv6Addr=valid_session_info.device.ipv6Address,
            usageThreshold=schemas.UsageThreshold(duration=valid_session_info.duration),
        )
        self.add_core_specific_parameters(valid_session_info, subscription)
        return subscription

    def create_qod_session(self, session_info: Dict) -> Dict:
        """
        Creates a QoS session based on CAMARA QoD API input.

        args:
            session_info: Dictionary containing session details conforming to
                          the CAMARA QoD session creation parameters.

        returns:
            dictionary containing the created session details, including its ID.
        """
        subscription = self._build_subscription(session_info)
        return common.as_session_with_qos_post(
            self.base_url, self.scs_as_id, subscription
        )

    def get_qod_session(self, session_id: str) -> Dict:
        """
        Retrieves details of a specific Quality on Demand (QoS) session.

        args:
            session_id: The unique identifier of the QoS session.

        returns:
            Dictionary containing the details of the requested QoS session.
        """
        session = common.as_session_with_qos_get(
            self.base_url, self.scs_as_id, session_id=session_id
        )
        log.info(f"QoD session retrived successfully [id={session_id}]")
        return session

    def delete_qod_session(self, session_id: str) -> None:
        """
        Deletes a specific Quality on Demand (QoS) session.

        args:
            session_id: The unique identifier of the QoS session to delete.

        returns:
            None
        """
        common.as_session_with_qos_delete(
            self.base_url, self.scs_as_id, session_id=session_id
        )
        log.info(f"QoD session deleted successfully [id={session_id}]")

    # Placeholder for other CAMARA APIs (e.g., Traffic Influence,
    # Location-retrieval, etc.)
