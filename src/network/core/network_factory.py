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
from __future__ import annotations

from typing import TYPE_CHECKING

from src.network.clients.oai.client import NetworkManager as OaiNefClient
from src.network.clients.open5gcore.client import NetworkManager as Open5GCoreClient
from src.network.clients.open5gs.client import NetworkManager as Open5GSClient

if TYPE_CHECKING:
    from .network_interface import NetworkManagementInterface


class NetworkClientFactory:
    """
    Factory class for creating Network Management Clients.
    """

    @staticmethod
    def create_network_client(
        client_name: str, base_url: str, scs_as_id: str
    ) -> NetworkManagementInterface:
        """
        Creates and returns an instance of the specified Network Client.
        """
        try:
            constructor = NetworkClientTypes.network_types[client_name]
            network_client_instance = constructor(base_url, scs_as_id)
            return network_client_instance
        except KeyError:
            # Get the list of supported client names
            supported_clients = list(NetworkClientTypes.network_types.keys())
            raise ValueError(
                f"Invalid network client name: '{client_name}'. "
                "Supported clients are: "
                f"{', '.join(supported_clients)}"
            )


class NetworkClientTypes:
    """
    Class for creating Network Clients.
    """

    OPEN5GS = "open5gs"
    OAI = "oai"
    OPEN5GCORE = "open5gcore"

    # --- Dictionary mapping type constants to constructors ---
    network_types = {
        OPEN5GS: lambda url, scs_as_id: Open5GSClient(
            base_url=url, scs_as_id=scs_as_id
        ),
        OAI: lambda url, scs_as_id: OaiNefClient(base_url=url, scs_as_id=scs_as_id),
        OPEN5GCORE: lambda url, scs_as_id: Open5GCoreClient(
            base_url=url, scs_as_id=scs_as_id
        ),
    }
