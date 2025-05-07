##
# Copyright (c) 2025 Netsoft Group, EURECOM.
# All rights reserved.
#
# This file is part of the Open SDK
#
# Contributors:
#   - Giulio Carota (giulio.carota@eurecom.fr)
##


from src.network.clients.oai.schemas import (
    CamaraQoDSessionInfo,
    CamaraTrafficInfluence,
    OaiAsSessionWithQosSubscription,
    TrafficInfluSub,
)


def camara_qod_to_as_session_with_qos(
    qod_input: CamaraQoDSessionInfo,
) -> OaiAsSessionWithQosSubscription:
    device_ip = qod_input.retrieve_ue_ipv4()
    server_ip = qod_input.retrieve_app_ipv4()

    # Extract callback sink and QoS profile
    sink_url = qod_input.sink
    qos_profile = qod_input.qosProfile

    # build flow descriptor in oai format using device ip and server ip
    flow_descriptor = f"permit out ip from {device_ip}/32 to {server_ip}/32"

    # create the nef request model
    nef_req = OaiAsSessionWithQosSubscription.construct()
    nef_req.ueIpv4Addr = device_ip
    nef_req.notificationDestination = sink_url
    nef_req.add_flow_descriptor(flow_desriptor=flow_descriptor)
    nef_req.qosReference = qos_profile
    nef_req.add_snssai(1, "FFFFFF")

    # the qos duration feature is not available yet in oai
    # nef_req.qosDuration = qod_input.duration

    return nef_req


def as_session_with_qos_to_camara_qod(
    nef_input: OaiAsSessionWithQosSubscription,
) -> CamaraQoDSessionInfo:
    # create the camara qod model

    qod_info = CamaraQoDSessionInfo.construct()

    flowDesc = nef_input.flowInfo[0].flowDescriptions[0]
    serverIp = flowDesc.split("to ")[1].split("/32")[0]

    qod_info.add_server_ipv4(serverIp)
    qod_info.qosProfile = nef_input.qosReference
    qod_info.add_ue_ipv4(nef_input.ueIpv4Addr)
    qod_info.sink = nef_input.notificationDestination
    qod_info.duration = nef_input.qosDuration

    return qod_info


def camara_ti_to_3gpp_ti(ti_input: CamaraTrafficInfluence) -> TrafficInfluSub:

    device_ip = ti_input.retrieve_ue_ipv4()
    server_ip = (
        ti_input.appInstanceId
    )  # assume that the instance id corresponds to its IPv4 address
    sink_url = ti_input.notificationSink.sink
    edge_zone = ti_input.edgeCloudZoneId

    # build flow descriptor in oai format using device ip and server ip
    flow_descriptor = f"permit out ip from {device_ip}/32 to {server_ip}/32"

    nef_traffic_influence = TrafficInfluSub.model_construct()
    nef_traffic_influence.afAppId = ti_input.appId
    nef_traffic_influence.afServiceId = "aa"
    nef_traffic_influence.ipv4Addr = device_ip
    nef_traffic_influence.notificationDestination = sink_url
    nef_traffic_influence.add_flow_descriptor(flow_desriptor=flow_descriptor)
    nef_traffic_influence.add_traffic_route(dnai=edge_zone)
    nef_traffic_influence.add_snssai(1, "FFFFFF")
    nef_traffic_influence.dnn = "oai"

    return nef_traffic_influence
