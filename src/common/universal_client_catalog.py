from typing import Dict

from src.common.universal_catalog import universal_client_catalog


class UniversalClientCatalog:
    @staticmethod
    def create_clients(specs: Dict[str, Dict[str, str]]) -> Dict[str, object]:
        """
        Create and return a dictionary of instantiated edgecloud/network/o-ran clients
        based on the provided specifications.

        Args:
            client_specs (list[dict]): A list of dictionaries, where each dictionary
                                    specifies a client to be created.
                                    Each client dictionary must contain:
                                    - 'domain' (str): The client's domain (e.g., 'edgecloud', 'network').
                                    - 'client_name' (str): The specific name of the client
                                                            (e.g., 'i2edge', 'open5gs').
                                    - 'base_url' (str): The base URL for the client's API.
                                    Optional parameters (like 'scs_as_id') can also be included
                                    if required by the specific client's constructor.

        Returns:
            dict: A dictionary where keys are the 'client_name' (str) and values are
                the instantiated client objects.

        Example:
            >>> from src.common.universal_client_catalog import UniversalClientCatalog
            >>>
            >>> client_specs_example = [
            >>>     {
            >>>         'domain': 'edgecloud',
            >>>         'client_name': 'i2edge',
            >>>         'base_url': 'http://localhost:8081',
            >>>         'description': 'i2edge client example.'
            >>>     },
            >>>     {
            >>>         'domain': 'network',
            >>>         'client_name': 'open5gs',
            >>>         'base_url': 'http://localhost:8084',
            >>>         'scs_as_id': 'my_unique_scs_id_example' # Example of optional parameter
            >>>     }
            >>> ]
            >>>
            >>> clients = invoke_clients(client_specs_example)
            >>> # Access a client: i2edge_client = clients['i2edge']
        """
        clients = {}
        for domain, config in specs.items():
            client_name = config["client_name"]
            base_url = config["base_url"]
            client = universal_client_catalog.get_client(domain, client_name, base_url)
            clients[domain] = client
        return clients
