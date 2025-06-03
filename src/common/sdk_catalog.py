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
        # TODO: uncomment when missing PiEdge's imports are added
        # "piedge": lambda url: PiEdgeClient(base_url=url),
    }
    try:
        return edge_cloud_factory[client_name](base_url)
    except KeyError:
        raise ValueError(
            f"Invalid edgecloud client '{client_name}'. Available: {list(edge_cloud_factory)}"
        )


def _network_catalog(client_name: str, base_url: str, scs_as_id: str):
    network_factory = {
        "open5gs": lambda url, scs_id: Open5GSClient(base_url=url, scs_as_id=scs_id),
        "oai": lambda url, scs_id: OaiCoreClient(base_url=url, scs_as_id=scs_id),
        "open5gcore": lambda url, scs_id: Open5GCoreClient(
            base_url=url, scs_as_id=scs_id
        ),
    }
    try:
        return network_factory[client_name](base_url, scs_as_id)
    except KeyError:
        raise ValueError(
            f"Invalid network client '{client_name}'. Available: {list(network_factory)}"
        )


# def _oran_catalog(client_name: str, base_url: str):
#     # TODO


class SdkClientCatalog:
    _domain_factories = {
        "edgecloud": _edgecloud_catalog,
        "network": _network_catalog,
        # "oran": _oran_catalog,
    }

    @classmethod
    def get_client(cls, domain: str, client_name: str, base_url: str, **kwargs):
        try:
            catalog = cls._domain_factories[domain]
        except KeyError:
            raise ValueError(
                f"Unsupported domain '{domain}'. Supported: {list(cls._domain_factories)}"
            )

        if domain == "network":
            if "scs_as_id" not in kwargs:
                raise ValueError("Missing required 'scs_as_id' for network clients.")
            return catalog(client_name, base_url, kwargs["scs_as_id"])
        else:
            return catalog(client_name, base_url)
