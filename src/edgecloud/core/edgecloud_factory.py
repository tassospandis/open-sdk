#!/usr/bin/env python3
# -*- coding: utf-8 -*-
##
# Copyright 2025-present by Software Networks Area, i2CAT.
# All rights reserved.
#
# This file is part of the Open SDK
#
# Contributors:
#   - Adrián Pino Martínez (adrian.pino@i2cat.net)
#   - Sergio Giménez (sergio.gimenez@i2cat.net)
##
from __future__ import annotations

from typing import TYPE_CHECKING

from src.edgecloud.clients.aeros.client import EdgeApplicationManager as AerosClient
from src.edgecloud.clients.i2edge.client import EdgeApplicationManager as I2EdgeClient
from src.edgecloud.clients.piedge.client import EdgeApplicationManager as PiEdgeClient

if TYPE_CHECKING:
    from .edgecloud_interface import EdgeCloudInterface


class EdgeCloudFactory:
    """
    Factory class for creating EdgeCloud Clients
    """

    @staticmethod
    def create_edgecloud_client(
        client_name: str, base_url: str
    ) -> EdgeCloudInterface:
        try:
            return EdgeCloudTypes.edgecloud_types[client_name](base_url)
        except KeyError:
            # Get the list of supported client names
            supported_clients = list(EdgeCloudTypes.edgecloud_types.keys())
            raise ValueError(
                f"Invalid edgecloud client name: '{client_name}'. "
                f"Supported clients are: {', '.join(supported_clients)}"
            )


class EdgeCloudTypes:
    """
    Class dedicated for the different types of edgecloud clients.
    """

    I2EDGE = "i2edge"
    AEROS = "aeros"
    PIEDGE = "piedge"

    edgecloud_types = {
        I2EDGE: lambda url: I2EdgeClient(base_url=url),
        AEROS: lambda url: AerosClient(base_url=url),
        PIEDGE: lambda url: PiEdgeClient(base_url=url),
    }
