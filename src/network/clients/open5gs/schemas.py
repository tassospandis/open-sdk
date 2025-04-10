# This file defines the Pydantic models that represent the data structures (schemas)
# for the requests sent to and responses received from the Open5GS NEF API,
# specifically focusing on the APIs needed to support CAMARA QoD.

import ipaddress
from enum import Enum
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field, NonNegativeInt, RootModel
from pydantic_extra_types.mac_address import MacAddress


class FlowDirection(Enum):
    """
    DOWNLINK: The corresponding filter applies for traffic to the UE.
    UPLINK: The corresponding filter applies for traffic from the UE.
    BIDIRECTIONAL: The corresponding filter applies for traffic both to and from the UE.
    UNSPECIFIED: The corresponding filter applies for traffic to the UE (downlink), but has no specific direction declared. The service data flow detection shall apply the filter for uplink traffic as if the filter was bidirectional. The PCF shall not use the value UNSPECIFIED in filters created by the network in NW-initiated procedures. The PCF shall only include the value UNSPECIFIED in filters in UE-initiated procedures if the same value is received from the SMF.
    """

    DOWNLINK = "DOWNLINK"
    UPLINK = "UPLINK"
    BIDIRECTIONAL = "BIDIRECTIONAL"
    UNSPECIFIED = "UNSPECIFIED"


class RequestedQosMonitoringParameter(Enum):
    DOWNLINK = "DOWNLINK"
    UPLINK = "UPLINK"
    ROUND_TRIP = "ROUND_TRIP"


class ReportingFrequency(Enum):
    EVENT_TRIGGERED = "EVENT_TRIGGERED"
    PERIODIC = "PERIODIC"
    SESSION_RELEASE = "SESSION_RELEASE"


Uinteger = Annotated[int, Field(ge=0)]


class DurationSec(RootModel[NonNegativeInt]):
    root: NonNegativeInt = Field(
        ...,
        description="Unsigned integer identifying a period of time in units of seconds.",
    )


class Volume(RootModel[NonNegativeInt]):
    root: NonNegativeInt = Field(
        ..., description="Unsigned integer identifying a volume in units of bytes."
    )


class SupportedFeatures(RootModel[str]):
    root: str = Field(
        ...,
        pattern=r"^[A-Fa-f0-9]*$",
        description="Hexadecimal string representing supported features.",
    )


class Link(RootModel[str]):
    root: str = Field(
        ...,
        description="String formatted according to IETF RFC 3986 identifying a referenced resource.",
    )


class FlowDescriptionModel(RootModel[str]):
    root: str = Field(..., description="Defines a packet filter of an IP flow.")


class EthFlowDescription(BaseModel):
    destMacAddr: MacAddress | None = None
    ethType: str
    fDesc: FlowDescriptionModel | None = None
    fDir: FlowDirection | None = None
    sourceMacAddr: MacAddress | None = None
    vlanTags: list[str] | None = Field(None, max_items=2, min_items=1)
    srcMacAddrEnd: MacAddress | None = None
    destMacAddrEnd: MacAddress | None = None


class UsageThreshold(BaseModel):
    duration: DurationSec | None = None
    totalVolume: Volume | None = None
    downlinkVolume: Volume | None = None
    uplinkVolume: Volume | None = None


class SponsorInformation(BaseModel):
    sponsorId: str = Field(..., description="It indicates Sponsor ID.")
    aspId: str = Field(..., description="It indicates Application Service Provider ID.")


class WebsockNotifConfig(BaseModel):
    websocketUri: Link | None = None
    requestWebsocketUri: bool | None = Field(
        None,
        description="Set by the SCS/AS to indicate that the Websocket delivery is requested.",
    )


class QosMonitoringInformationModel(BaseModel):
    reqQosMonParams: list[RequestedQosMonitoringParameter] | None = Field(
        None, min_items=1
    )
    repFreqs: list[ReportingFrequency] | None = Field(None, min_items=1)
    repThreshDl: Uinteger | None = None
    repThreshUl: Uinteger | None = None
    repThreshRp: Uinteger | None = None
    waitTime: int | None = None
    repPeriod: int | None = None


class FlowInfo(BaseModel):
    flowId: int = Field(..., description="Indicates the IP flow.")
    flowDescriptions: list[str] | None = Field(
        None,
        description="Indicates the packet filters of the IP flow. Refer to subclause 5.3.8 of 3GPP TS 29.214 for encoding. It shall contain UL and/or DL IP flow description.",
        max_items=2,
        min_items=1,
    )


class AsSessionWithQoSSubscription(BaseModel):
    model_config = ConfigDict(serialize_by_alias=True)
    self_: Link | None = Field(None, alias="self")
    supportedFeatures: SupportedFeatures | None = None
    notificationDestination: Link
    flowInfo: list[FlowInfo] | None = Field(
        None, description="Describe the data flow which requires QoS.", min_items=1
    )
    ethFlowInfo: list[EthFlowDescription] | None = Field(
        None, description="Identifies Ethernet packet flows.", min_items=1
    )
    qosReference: str | None = Field(
        None, description="Identifies a pre-defined QoS information"
    )
    altQoSReferences: list[str] | None = Field(
        None,
        description="Identifies an ordered list of pre-defined QoS information. The lower the index of the array for a given entry, the higher the priority.",
        min_items=1,
    )
    ueIpv4Addr: ipaddress.Ipv4Addr | None = None
    ueIpv6Addr: ipaddress.Ipv6Addr | None = None
    macAddr: MacAddress | None = None
    usageThreshold: UsageThreshold | None = None
    sponsorInfo: SponsorInformation | None = None
    qosMonInfo: QosMonitoringInformationModel | None = None
    requestTestNotification: bool | None = Field(
        None,
        description="Set to true by the SCS/AS to request the SCEF to send a test notification as defined in subclause 5.2.5.3. Set to false or omitted otherwise.",
    )
    websockNotifConfig: WebsockNotifConfig | None = None


class CamaraQoDSessionInfo(BaseModel):
    """
    Represents the input data for creating a QoD session.
    """

    pass
