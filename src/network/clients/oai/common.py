##
# Copyright (c) 2025 Netsoft Group, EURECOM.
# All rights reserved.
#
# This file is part of the Open SDK
#
# Contributors:
#   - Giulio Carota (giulio.carota@eurecom.fr)
##


from pydantic import BaseModel
from src.network.clients.errors import NetworkPlatformError

import json
import requests

def _make_request(method: str, url: str, data=None):
    try:
        headers = None
        if method == 'POST' or method == 'PUT':
            headers = {
                "Content-Type": "application/json",
                "accept": "application/json",
            }
        elif method == 'GET':
            headers = {
                "accept": "application/json",
            }
        response = requests.request(method, url, headers=headers, data=data)
        response.raise_for_status()
        if response.content:
            return response.json()
    except requests.exceptions.HTTPError as e:
        raise OaiHttpError(e) from e
    except requests.exceptions.ConnectionError as e:
        raise OaiHttpError("connection error") from e


#QoD methods
def oai_as_session_with_qos_post(base_url: str, scs_as_id: str, model_payload: BaseModel) -> dict:
    data = model_payload.model_dump_json(exclude_none=True)
    url = oai_as_session_with_qos_build_url(base_url, scs_as_id)
    return _make_request("POST", url, data=data)


def oai_as_session_with_qos_get(base_url: str, scs_as_id: str, session_id: str) -> dict:
    url = oai_as_session_with_qos_build_url(base_url, scs_as_id, session_id)
    return _make_request("GET", url)


def oai_as_session_with_qos_delete(base_url: str, scs_as_id: str, session_id: str):
    url = oai_as_session_with_qos_build_url(base_url, scs_as_id, session_id)
    return _make_request("DELETE", url)

def oai_as_session_with_qos_build_url(base_url: str, scs_as_id: str, session_id: str = None):
    url = f"{base_url}/3gpp-as-session-with-qos/v1/{scs_as_id}/subscriptions"
    if session_id != None and len(session_id) > 0:
        return f"{url}/{session_id}"
    else:
        return url


## Traffic Influence methods
def oai_traffic_influence_post(base_url: str, scs_as_id: str, model_payload: BaseModel) -> dict:
    data = model_payload.model_dump_json(exclude_none=True)
    url = oai_traffic_influence_build_url(base_url, scs_as_id)
    return _make_request("POST", url, data=data)

def oai_traffic_influence_delete(base_url: str, scs_as_id: str, session_id: str):
    url = oai_traffic_influence_build_url(base_url, scs_as_id, session_id)
    return _make_request("DELETE", url)

def oai_traffic_influence_put(base_url: str, scs_as_id: str, session_id: str, model_payload: BaseModel) -> dict:
    data = model_payload.model_dump_json(exclude_none=True)
    url = oai_traffic_influence_build_url(base_url, scs_as_id, session_id)
    return _make_request("PUT", url, data=data)


def oai_traffic_influence_build_url(base_url: str, scs_as_id: str, session_id: str = None):
    url = f"{base_url}/3gpp-traffic-influence/v1/{scs_as_id}/subscriptions"
    if session_id != None and len(session_id) > 0:
        return f"{url}/{session_id}"
    else:
        return url

class OaiHttpError(Exception):
    pass

class OaiNetworkError(NetworkPlatformError):
    pass