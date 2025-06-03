from src.edgecloud.clients.aeros.client import EdgeApplicationManager as AerosClient
from src.edgecloud.clients.i2edge.client import EdgeApplicationManager as I2EdgeClient
from src.network.clients.oai.client import NetworkManager as OaiCoreClient
from src.network.clients.open5gcore.client import NetworkManager as Open5GCoreClient
from src.network.clients.open5gs.client import NetworkManager as Open5GSClient

# from src.edgecloud.clients.piedge.client import EdgeApplicationManager as PiEdgeClient


def _edgecloud_catalog(client_name: str, base_url: str):
    edge_cloud_factory = {
        "aeros": lambda url: AerosClient(base_url=url),
        "i2edge": lambda url: I2EdgeClient(base_url=url),
        # "piedge": lambda url: PiEdgeClient(base_url=url),
    }
    try:
        return edge_cloud_factory[client_name](base_url)
    except KeyError:
        raise ValueError(
            f"Invalid edgecloud client '{client_name}'. Available: {list(edge_cloud_factory)}"
        )


def _network_catalog(client_name: str, base_url: str):
    network_factory = {
        "open5gs": lambda url: Open5GSClient(base_url=url),
        "oai": lambda url: OaiCoreClient(base_url=url),
        "open5gcore": lambda url: Open5GCoreClient(base_url=url),
    }
    try:
        return network_factory[client_name](base_url)
    except KeyError:
        raise ValueError(
            f"Invalid network client '{client_name}'. Available: {list(network_factory)}"
        )


class UniversalClientCatalog:
    _domain_factories = {
        "edgecloud": _edgecloud_catalog,
        "network": _network_catalog,
    }

    @classmethod
    def get_client(cls, domain: str, client_name: str, base_url: str):
        try:
            catalog = cls._domain_factories[domain]
        except KeyError:
            raise ValueError(
                f"Unsupported domain '{domain}'. Supported: {list(cls._domain_factories)}"
            )
        return catalog(client_name, base_url)


universal_client_catalog = UniversalClientCatalog()
