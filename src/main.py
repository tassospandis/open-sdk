from src.edgecloud.core.edgecloud_factory import EdgeCloudFactory

# def create_edgecloud_client(client_name: str, base_url: str):
#     """
#     Create and return an edgecloud client.

#     Args:
#         client_name (str): The name of the client (e.g., "i2edge").
#         base_url (str): The base URL for the client.

#     Returns:
#         The created edgecloud client.
#     """
#     return EdgeCloudFactory.create_edgecloud_client(client_name, base_url)

####################################################################################################
# Temporal code - testing purposes
####################################################################################################
if __name__ == "__main__":
    # Define the client name and base URL
    client_name = "i2edge"
    base_url = "http://192.168.123.237:30769/"

    # Create the edgecloud client
    sbi = EdgeCloudFactory.create_edgecloud_client(client_name, base_url)
    
    # Print the edgecloud client being used and its URL
    print(f"Using edgecloud client: {sbi}")
    print(f"URL: {sbi.base_url}")

    # Call the get_edge_cloud_zones function
    zones = sbi.get_edge_cloud_zones()
    print(f"Edge Cloud Zones: {zones}")
####################################################################################################
# End of Temporal code
####################################################################################################
