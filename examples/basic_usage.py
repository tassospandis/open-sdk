from src.common.sdk_catalog_client import SdkCatalogClient

# "src.common.universal_catalog_client" would be equivalent to "sunrise6g_opensdk"


def main():
    # The module importing the SDK, loads the config
    client_specs = {
        "edgecloud": {
            "client_name": "i2edge",
            "base_url": "http://192.168.123.237:30769/",
        }
        # ,
        # "network": {
        #     "client_name": "open5gs",
        #     "base_url": "http://IP:PORT",
        #     "scs_as_id": "id_example"
        # }
    }

    clients = SdkCatalogClient.create_clients(client_specs)

    edgecloud_client = clients.get("edgecloud")
    # network_client = clients.get("network")

    # Example of edgecloud client in action
    print("Testing edgecloud client function: get_edge_cloud_zones:")
    zones = edgecloud_client.get_edge_cloud_zones()
    print(zones)

    # # Example of network client in action
    # print("Testing network client function: EXAMPLE_FUNCTION:")
    # network_client.get_qod_session(session_id="example_session_id")


if __name__ == "__main__":
    main()
