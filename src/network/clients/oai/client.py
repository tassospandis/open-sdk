from typing import Dict
from src import logger
import shortuuid
import time
from pydantic import ValidationError
from src.network.core.network_interface import NetworkManagementInterface
from src.network.clients.oai.schemas import CamaraQoDSessionInfo, OaiAsSessionWithQosSubscription
from src.network.clients.oai.common import (
    oai_as_session_with_qos_post,
    oai_as_session_with_qos_get,
    oai_as_session_with_qos_delete,
    OaiHttpError,
    OaiNetworkError
)

from src.network.clients.oai.utils import camara_qod_to_as_session_with_qos, as_session_with_qos_to_camara_qod

log = logger.get_logger(__name__)

class OaiNefClient(NetworkManagementInterface):
    def __init__(self, base_url: str, scs_as_id: str = None):
        """
        Initialize Network Client for OAI Core Network
        The currently supported features are:
         - QoD
         - Traffic Influence
        """
        try:
            super().__init__()
            self.base_url = base_url
            self.scs_as_id = shortuuid.uuid()
            log.info(f"Initialized OaiNefClient with base_url: {self.base_url} and scs_as_id: {self.scs_as_id}")
        except Exception as e:
            log.error(f"Failed to initialize OaiNefClient: {e}")
            raise e

    #implementation of the NetworkManagementInterface QoD Methods
    def create_qod_session(self, session_info: Dict) -> Dict:
        """
        Creates a QoS session based on CAMARA QoD API input.
        It maps CAMARA QoD API POST /sessions to
        OAI NEF POST /3gpp-as-session-with-qos/v1/{scs_as_id}/subscriptions
        """
        try:
            qod_input = CamaraQoDSessionInfo(**session_info)

            #convert CAMARA QoD to NEF AsSessionWithQos model and do POST
            nef_req = camara_qod_to_as_session_with_qos(qod_input)
            nef_res = oai_as_session_with_qos_post(self.base_url, self.scs_as_id, nef_req)

            #retrieve the NEF resource id
            if "self" in nef_res.keys():
                nef_url = nef_res["self"]
                nef_id = nef_url.split("subscriptions/")[1]
            else:
                raise OaiNetworkError("No valid ID for the created resource was returned")

            #create QoD session detail and return info with resource Id
            qod_input.sessionId = nef_id

            log.info(f"QoD session activated successfully [id={nef_id}]")

            return qod_input

        except ValidationError as e:
            raise OaiNetworkError("Could not validate QoD Session Info data") from e
        except KeyError as e:
            raise OaiNetworkError(f"Missing field in QoD Session Info data: {e}") from e
        except OaiHttpError as e:
            raise OaiNetworkError(f"The network could not enable the QoD Session. It returned {e}") from e
        except OaiNetworkError as e:
            raise


    def get_qod_session(self, session_id: str) -> Dict:
        """
        Retrieves details of a specific Quality on Demand (QoS) session.
        It maps CAMARA QoD API GET /sessions/{sessionId} to
        OAI NEF GET /3gpp-as-session-with-qos/v1/{scs_as_id}/subscriptions/{subscriptionId}
        """
        try:
            res = oai_as_session_with_qos_get(self.base_url, self.scs_as_id, session_id=session_id)
            nef_res = OaiAsSessionWithQosSubscription(**res)
            qod_info = as_session_with_qos_to_camara_qod(nef_res)

            log.info(f"QoD session retrived successfully [id={session_id}]")

            return qod_info
        except ValidationError as e:
            raise OaiNetworkError("Could not validate network response data") from e
        except OaiHttpError as e:
            raise OaiNetworkError(f"The network could not enable the QoD Session. It returned {e}") from e
        except OaiNetworkError as e:
            raise

    def delete_qod_session(self, session_id: str) -> None:
        """
        Deletes a specific Quality on Demand (QoS) session.
        It maps CAMARA QoD API DELETE /sessions/{sessionId} to
        OAI NEF DELETE /3gpp-as-session-with-qos/v1/{scs_as_id}/subscriptions/{subscriptionId}
        """
        try:
            oai_as_session_with_qos_delete(self.base_url, self.scs_as_id, session_id=session_id)

            log.info(f"QoD session deleted successfully [id={session_id}]")

        except OaiHttpError as e:
            raise OaiNetworkError(f"The network could not enable the QoD Session. It returned {e}") from e
        except OaiNetworkError as e:
            raise

    #implementation of the NetworkManagementInterface Traffic Influence Methods
    def create_traffic_influence_resource(self, traffic_influence_info):

        log.error(f"create_traffic_influence_resource not implemented yet")

        raise NotImplementedError()

    def delete_traffic_influence_resource(self, resource_id):

        log.error(f"delete_traffic_influence_resource not implemented yet")

        raise NotImplementedError()

    def get_traffic_influence_resource(self, resource_id):

        log.error(f"get_traffic_influence_resource not implemented yet")

        raise NotImplementedError()