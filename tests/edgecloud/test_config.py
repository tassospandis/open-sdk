# -*- coding: utf-8 -*-
"""
EdgeCloud Platform Test Configuration

This module contains shared configuration constants and manifests for testing
the EdgeCloud Platform integration across different clients.
"""

######################
# i2Edge variables
######################
# EdgeCloud Zone
ZONE_ID = "Omega12345"

# Artefact
ARTEFACT_ID = "i2edgechart-id-2"
ARTEFACT_NAME = "i2edgechart"
REPO_NAME = "github-cesar"
REPO_TYPE = "PUBLICREPO"
REPO_URL = "https://cesarcajas.github.io/helm-charts-examples/"

# Onboarding: CAMARA /app payload (only mandatory fields)
APP_ONBOARD_MANIFEST = {
    "appId": ARTEFACT_ID,
    "name": "i2edge-app-SDK",
    "version": "1.0.0",
    "appProvider": "i2CAT",
    "packageType": "CONTAINER",
    "appRepo": {
        "type": "PUBLICREPO",
        "imagePath": "https://example.com/my-app-image:1.0.0",
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
            "componentName": "my-component",
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
# TODO
