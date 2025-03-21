from src.edgecloud.core.edgecloud_factory import EdgeCloudFactory

def create_edgecloud_client(client_name: str, base_url: str):
    """
    Create and return an edgecloud client.

    Args:
        client_name (str): The name of the client (e.g., "i2edge").
        base_url (str): The base URL for the client.

    Returns:
        The created edgecloud client.
    """
    return EdgeCloudFactory.create_edgecloud_client(client_name, base_url)
