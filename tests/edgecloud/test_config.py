# -*- coding: utf-8 -*-
##
# Copyright 2025-present by Software Networks Area, i2CAT.
# All rights reserved.
#
# This file is part of the Open SDK
#
# Contributors:
#   - Adrián Pino Martínez (adrian.pino@i2cat.net)
#   - Sergio Giménez (sergio.gimenez@i2cat.net)
##
"""
EdgeCloud Platform Test Configuration

This file contains the configuration constants and manifests for testing
the EdgeCloud Platform integration across different clients.
"""

######################
# i2Edge variables
######################
# EdgeCloud Zone
ZONE_ID = "urn:ngsi-ld:Domain:NCSRD"

# Artefact
ARTEFACT_ID = "aeros-app-1"
ARTEFACT_NAME = "i2edgechart"
REPO_NAME = "github-cesar"
REPO_TYPE = "PUBLICREPO"
REPO_URL = "https://cesarcajas.github.io/helm-charts-examples/"

# Onboarding: CAMARA /app payload (only mandatory fields)
APP_ONBOARD_MANIFEST = {
    "appId": ARTEFACT_ID,
    "name": "aeros-SDK-app",
    "version": "1.0.0",
    "appProvider": "ncsrd",
    "packageType": "CONTAINER",
    "appRepo": {
        "type": "PUBLICREPO",
        "imagePath": "docker.io/library/nginx:latest",
    },
    "requiredResources": {
        "infraKind": "kubernetes",
        "applicationResources": {
            "cpuPool": {
                "numCPU": 2,
                "memory": 2048,
                "topology": {
                    "minNumberOfNodes": 2,
                    "minNodeCpu": 1,
                    "minNodeMemory": 1024,
                },
            }
        },
        "isStandalone": False,
        "version": "1.29",
    },
    "componentSpec": [
        {
            "componentName": "aeros-comp",
            "networkInterfaces": [
                {
                    "interfaceId": "eth0",
                    "protocol": "TCP",
                    "port": 8080,
                    "visibilityType": "VISIBILITY_EXTERNAL",
                }
            ],
        }
    ],
}

# App deployment config
APP_ID = ARTEFACT_ID
APP_ZONES = [
    {
        "kubernetesClusterRef": "not-used",
        "EdgeCloudZone": {
            "edgeCloudZoneId": ZONE_ID,
            "edgeCloudZoneName": "not-used",
            "edgeCloudZoneStatus": "not-used",
            "edgeCloudProvider": "not-used",
            "edgeCloudRegion": "not-used",
        },
    }
]

######################
# PiEdge variables
######################
# TODO

######################
# aerOS variables
######################
AEROS_ZONE_ID = "urn:ngsi-ld:Domain:NCSRD"
