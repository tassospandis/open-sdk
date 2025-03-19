from __future__ import annotations
from enum import Enum
from typing import TYPE_CHECKING

from src.edgecloud.clients.i2edge.client import EdgeApplicationManager as I2EdgeClient
from src.edgecloud.clients.aeros.client import EdgeApplicationManager as AerosClient
from src.edgecloud.clients.piedge.client import EdgeApplicationManager as PiEdgeClient
from src.edgecloud.clients.dmo.client import EdgeApplicationManager as DmoClient

if TYPE_CHECKING:
    from .edgecloud_interface import EdgeCloudInterface

class EdgeCloudFactory:
    """
    Factory class for creating EdgeCloud Clients
    """

    @staticmethod
    def create_edgecloud_client(client_name: str, base_url: str) -> EdgeCloudInterface:
        try:
            return EdgeCloudTypes.edgecloud_types[client_name](base_url)
        except KeyError:
            # Get the list of supported client names
            supported_clients = list(EdgeCloudTypes.edgecloud_types.keys())
            raise ValueError(
                f"Invalid edgecloud client name: '{client_name}'. "
                f"Supported clients are: {', '.join(supported_clients)}"
            )
        
class EdgeCloudTypes():
    """
    Class dedicated for the different types of edgecloud clients.
    """
    I2EDGE = "i2edge"
    AEROS = "aeros"
    DMO = "dmo"
    PIEDGE="piedge"

    edgecloud_types = {
        I2EDGE: lambda url: I2EdgeClient(base_url=url),
        AEROS: lambda url: AerosClient(base_url=url),
        DMO: lambda url: DmoClient(base_url=url),
        PIEDGE: lambda url: PiEdgeClient(base_url=url)
    }
