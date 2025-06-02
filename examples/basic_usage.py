from src.common.universal_client_catalog import UniversalClientCatalog


def main():
    # Hardcoded client configuration; here we would expect to load the config
    client_specs = {
        "edgecloud": {
            "client_name": "i2edge",
            "base_url": "http://192.168.123.237:30769/",
        }
        # ,
        # "network": {
        #     "client_name": "open5gs",
        #     "base_url": "http://IP:PORT"
        # }
    }

    clients = UniversalClientCatalog.create_clients(client_specs)

    edgecloud_client = clients.get("edgecloud")
    # network_client = clients.get("network")

    # Example usage
    print("Running test endpoint: get_edge_cloud_zones:")
    zones = edgecloud_client.get_edge_cloud_zones()
    print(zones)


if __name__ == "__main__":
    main()
