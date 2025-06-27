#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Pydantic data models for CAMARA Edge Application Management API (version 0.9.3-wip).
These schemas reflect the structure of requests and responses defined in the OpenAPI specification.
"""

from enum import Enum
from typing import List, Optional, Union
from uuid import UUID

from pydantic import BaseModel, Field


# --- ENUMS ---
class PackageType(str, Enum):
    QCOW2 = "QCOW2"
    OVA = "OVA"
    CONTAINER = "CONTAINER"
    HELM = "HELM"


class VisibilityType(str, Enum):
    VISIBILITY_EXTERNAL = "VISIBILITY_EXTERNAL"
    VISIBILITY_INTERNAL = "VISIBILITY_INTERNAL"


class Protocol(str, Enum):
    TCP = "TCP"
    UDP = "UDP"
    ANY = "ANY"


class AppInstanceStatus(str, Enum):
    READY = "ready"
    INSTANTIATING = "instantiating"
    FAILED = "failed"
    TERMINATING = "terminating"
    UNKNOWN = "unknown"


# --- NESTED SCHEMAS ---
class AppRepo(BaseModel):
    type: str
    imagePath: str
    userName: Optional[str]
    credentials: Optional[str]
    authType: Optional[str]
    checksum: Optional[str]


class NetworkInterface(BaseModel):
    interfaceId: str = Field(..., pattern=r"^[A-Za-z][A-Za-z0-9_]{3,31}$")
    protocol: Protocol
    port: int = Field(..., ge=1, le=65535)
    visibilityType: VisibilityType


class ComponentSpec(BaseModel):
    componentName: str
    networkInterfaces: List[NetworkInterface]


class CpuTopology(BaseModel):
    minNumberOfNodes: int
    minNodeCpu: int
    minNodeMemory: int


class CpuPool(BaseModel):
    numCPU: int
    memory: int
    topology: CpuTopology


class GpuTopology(BaseModel):
    minNumberOfNodes: int
    minNodeCpu: int
    minNodeMemory: int
    minNodeGpuMemory: int


class GpuPool(BaseModel):
    numCPU: int
    memory: int
    gpuMemory: int
    topology: GpuTopology


class KubernetesResources(BaseModel):
    infraKind: str = Field("kubernetes", Literal=True)
    applicationResources: Optional[dict]
    isStandalone: Optional[bool]
    version: Optional[str]
    additionalStorage: Optional[str]
    networking: Optional[dict]
    addons: Optional[dict]


class VmResources(BaseModel):
    infraKind: str = Field("virtualMachine", Literal=True)
    numCPU: int
    memory: int
    additionalStorages: Optional[List[dict]]
    gpu: Optional[dict]


class ContainerResources(BaseModel):
    infraKind: str = Field("container", Literal=True)
    numCPU: str  # vCPU in formats like "1", "0.5", or "500m"
    memory: int
    storage: Optional[List[dict]]
    gpu: Optional[dict]


class DockerComposeResources(BaseModel):
    infraKind: str = Field("dockerCompose", Literal=True)
    numCPU: int
    memory: int
    storage: Optional[List[dict]]
    gpu: Optional[dict]


RequiredResources = Union[
    KubernetesResources, VmResources, ContainerResources, DockerComposeResources
]


# --- PRIMARY SCHEMAS ---
class AppManifest(BaseModel):
    name: str = Field(..., pattern=r"^[A-Za-z][A-Za-z0-9_]{1,63}$")
    version: str
    appProvider: str = Field(..., pattern=r"^[A-Za-z][A-Za-z0-9_]{7,63}$")
    packageType: PackageType
    appRepo: AppRepo
    requiredResources: RequiredResources
    componentSpec: List[ComponentSpec]


class AppInstanceDeploymentRequest(BaseModel):
    name: str = Field(..., pattern=r"^[A-Za-z][A-Za-z0-9_]{1,63}$")
    appId: UUID
    edgeCloudZoneId: UUID
    kubernetesClusterRef: Optional[UUID] = None


class ComponentEndpoint(BaseModel):
    interfaceId: str
    accessPoints: dict  # Can be refined based on AccessEndpoint schema


class AppInstanceInfo(BaseModel):
    name: str
    appId: UUID
    appInstanceId: UUID
    appProvider: str
    edgeCloudZoneId: UUID
    status: AppInstanceStatus = AppInstanceStatus.UNKNOWN
    componentEndpointInfo: Optional[List[ComponentEndpoint]] = None
    kubernetesClusterRef: Optional[UUID] = None
