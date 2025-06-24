from sunrise6g_opensdk.edgecloud.adapters.kubernetes.lib.models.deploy_service_function import (  # noqa: E501
    DeployServiceFunction,
)
from sunrise6g_opensdk.edgecloud.adapters.kubernetes.lib.utils import (
    auxiliary_functions,
)
from sunrise6g_opensdk.edgecloud.adapters.kubernetes.lib.utils.connector_db import (
    ConnectorDB,
)
from sunrise6g_opensdk.edgecloud.adapters.kubernetes.lib.utils.kubernetes_connector import (
    KubernetesConnector,
)

driver = None


def deploy_service_function(
    service_function: DeployServiceFunction,
    connector_db: ConnectorDB,
    kubernetes_connector: KubernetesConnector,
    paas_name=None,
):

    # descriptor_paas_input["scaling_type"]="minimize_cost"
    # print(descriptor_paas_input)
    # we need to create the descriptor_paas_ needed for deployment
    # search if app exists in the catalogue

    ser_function_ = connector_db.get_documents_from_collection(
        "service_functions",
        input_type="name",
        input_value=service_function.service_function_name,
    )
    if not ser_function_:
        return "The given service function does not exist in the catalogue"

    final_deploy_descriptor = {}
    deployed_name = service_function.service_function_instance_name
    deployed_name = auxiliary_functions.prepare_name(deployed_name, driver)
    final_deploy_descriptor["name"] = deployed_name

    final_deploy_descriptor["location"] = service_function.location

    containers = []
    con_ = {}
    con_["image"] = ser_function_[0]["image"]
    application_ports = ser_function_[0].get("application_ports")
    con_["application_ports"] = application_ports

    if service_function.node_ports is not None:
        exposed_ports = auxiliary_functions.return_equal_ignore_order(
            application_ports, service_function.node_ports
        )
        if exposed_ports:

            con_["exposed_ports"] = exposed_ports
    containers.append(con_)

    final_deploy_descriptor["containers"] = containers

    response = kubernetes_connector.deploy_service_function(final_deploy_descriptor)
    # insert it to mongo db
    deployed_service_function_db = {}
    deployed_service_function_db["service_function_name"] = ser_function_[0]["name"]
    deployed_service_function_db["location"] = service_function.location
    deployed_service_function_db["instance_name"] = deployed_name

    if isinstance(response, dict) and response.get("status") == "success":
        connector_db.insert_document_deployed_service_function(
            document=deployed_service_function_db
        )

    return response
