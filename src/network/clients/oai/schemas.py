##
# Copyright (c) 2025 Netsoft Group, EURECOM.
# All rights reserved.
#
# This file is part of the Open SDK
#
# Contributors:
#   - Giulio Carota (giulio.carota@eurecom.fr)
##

from pydantic import BaseModel, Field, AnyHttpUrl
from typing import List, Optional


class Snssai(BaseModel):
    sst: int = Field(default=1)
    sd: str = Field(default="FFFFFF")

class FlowInfoItem(BaseModel):
    flowId: int
    flowDescriptions: List[str]

class OaiAsSessionWithQosSubscription(BaseModel):
    """
    Represents the model to create an AsSessionWithQoS resource inside the OAI NEF.
    """
    supportedFeatures: str = Field(default="12")
    dnn: str = Field(default="oai")
    snssai: Snssai
    flowInfo: List[FlowInfoItem]
    ueIpv4Addr: str
    notificationDestination: str
    qosReference: str
    self: Optional[str] = None
    qosDuration: Optional[int] = None

    def add_flow_descriptor(self, flow_desriptor: str):
        self.flowInfo = list()
        self.flowInfo.append(FlowInfoItem(
            flowId=len(self.flowInfo)+1,
            flowDescriptions=[flow_desriptor]
        ))

    def add_snssai(self, sst: int, sd: str = None):
        self.snssai = Snssai(sst=sst, sd=sd)

class PortRange(BaseModel):
    from_: int = Field(alias="from")
    to: int

    class Config:
        populate_by_name = True

class Ports(BaseModel):
    ranges: Optional[List[PortRange]] = None
    ports: Optional[List[int]] = None

class Ipv4Address(BaseModel):
    publicAddress: str
    publicPort: Optional[int] = None

class Device(BaseModel):
    phoneNumber: Optional[str] = None
    networkAccessIdentifier: Optional[str] = None
    ipv4Address: Optional[Ipv4Address] = None
    ipv6Address: Optional[str] = None

class ApplicationServer(BaseModel):
    ipv4Address: Optional[str] = None
    ipv6Address: Optional[str] = None

class SinkCredential(BaseModel):
    credentialType: Optional[str] = None

class CamaraQoDSessionInfo(BaseModel):
    """
    Represents the input data for creating a QoD session.
    """
    duration: int
    qosProfile: str
    applicationServer: ApplicationServer

    device: Optional[Device] = None
    devicePorts: Optional[Ports] = None
    applicationServerPorts: Optional[Ports] = None
    sink: Optional[str] = None
    sinkCredential: Optional[SinkCredential] = None

    #fields only applicable to sessionInfo in responses:
    sessionId: Optional[str] = None
    startedAt: Optional[int] = None
    expiresAt: Optional[int] = None
    qosStatus: Optional[str] = None
    statusInfo: Optional[str] = None


    class Config:
        populate_by_name = True

    def retrieve_ue_ipv4(self):
        if self.device is not None and self.device.ipv4Address is not None:
            return self.device.ipv4Address.publicAddress
        else:
            raise KeyError("device.ipv4Address.publicAddress")

    def retrieve_app_ipv4(self):
        if self.applicationServer.ipv4Address is not None:
            return self.applicationServer.ipv4Address
        else:
            raise KeyError("applicationServer.ipv4Address")

    def add_server_ipv4(self, ipv4: str):
        self.applicationServer = ApplicationServer(ipv4Address = ipv4)


    def add_ue_ipv4(self, ipv4: str):
        if self.device is None:
            self.device = Device()
        if self.device.ipv4Address is None:
            self.device.ipv4Address = Ipv4Address(publicAddress=ipv4)