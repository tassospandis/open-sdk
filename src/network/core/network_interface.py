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
from typing import Dict


class NetworkManagementInterface(ABC):
    """
    Abstract Base Class for Network Resource Management.

    This interface defines the standard methods that all
    Network Clients (Open5GS, OAI, Open5GCore) must implement.

    Partners implementing a new network client should inherit from this class
    and provide concrete implementations for all abstract methods relevant
    to their specific NEF capabilities.
    """

    @abstractmethod
    def create_qod_session(self, session_info: Dict) -> Dict:
        """
        Creates a QoS session based on CAMARA QoD API input.

        args:
            session_info: Dictionary containing session details conforming to
                          the CAMARA QoD session creation parameters.

        returns:
            dictionary containing the created session details, including its ID.
        """
        pass

    @abstractmethod
    def get_qod_session(self, session_id: str) -> Dict:
        """
        Retrieves details of a specific Quality on Demand (QoS) session.

        args:
            session_id: The unique identifier of the QoS session.

        returns:
            Dictionary containing the details of the requested QoS session.
        """
        pass

    @abstractmethod
    def delete_qod_session(self, session_id: str) -> None:
        """
        Deletes a specific Quality on Demand (QoS) session.

        args:
            session_id: The unique identifier of the QoS session to delete.

        returns:
            None
        """
        pass

    @abstractmethod
    def create_traffic_influence_resource(self, traffic_influence_info: Dict) -> Dict:
        """
        Creates a Traffic Influence resource based on CAMARA TI API input.

        args:
            traffic_influence_info: Dictionary containing traffic influence details conforming to
                                    the CAMARA TI resource creation parameters.

        returns:
            dictionary containing the created traffic influence resource details, including its ID.
        """
        pass

    @abstractmethod
    def put_traffic_influence_resource(
        self, resource_id: str, traffic_influence_info: Dict
    ) -> Dict:
        """
        Retrieves details of a specific Traffic Influence resource.

        args:
            resource_id: The unique identifier of the Traffic Influence resource.

        returns:
            Dictionary containing the details of the requested Traffic Influence resource.
        """
        pass

    @abstractmethod
    def delete_traffic_influence_resource(self, resource_id: str) -> None:
        """
        Deletes a specific Traffic Influence resource.

        args:
            resource_id: The unique identifier of the Traffic Influence resource to delete.

        returns:
            None
        """
        pass

    # Placeholder for other CAMARA APIs (e.g., Traffic Influence,
    # Location-retrieval, etc.)
