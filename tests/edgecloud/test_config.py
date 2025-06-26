# -*- coding: utf-8 -*-
"""
EdgeCloud Platform Test Configuration

This file contains the configuration constants and manifests for testing
the EdgeCloud Platform integration across different adapters.
"""

CONFIG = {
    "i2edge": {
        "ZONE_ID": "Omega",
        "ARTEFACT_ID": "i2edgechart-id-2",
        "ARTEFACT_NAME": "i2edgechart",
        "REPO_NAME": "github-cesar",
        "REPO_TYPE": "PUBLICREPO",
        "REPO_URL": "https://cesarcajas.github.io/helm-charts-examples/",
        "APP_ONBOARD_MANIFEST": {
            "appId": "i2edgechart-id-2",
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
        },
        "APP_ID": "i2edgechart-id-2",
        "APP_ZONES": [
            {
                "kubernetesClusterRef": "not-used",
                "EdgeCloudZone": {
                    "edgeCloudZoneId": "Omega",
                    "edgeCloudZoneName": "not-used",
                    "edgeCloudZoneStatus": "not-used",
                    "edgeCloudProvider": "not-used",
                    "edgeCloudRegion": "not-used",
                },
            }
        ],
    },
    "aeros": {
        "ZONE_ID": "urn:ngsi-ld:Domain:NCSRD",
        "ARTEFACT_ID": "aeros-app-2",
        "ARTEFACT_NAME": "aeroschart",
        "REPO_NAME": "github-aeros",
        "REPO_TYPE": "PUBLICREPO",
        "REPO_URL": "https://aeros.github.io/helm/",
        "APP_ONBOARD_MANIFEST": {
            "appId": "aeros-app-2",
            "name": "aeros-SDK-app",
            "version": "1.0.0",
            "appProvider": "aeros",
            "packageType": "CONTAINER",
            "appRepo": {
                "type": "PUBLICREPO",
                "imagePath": "docker.io/library/nginx:stable",
            },
            "requiredResources": {
                "infraKind": "kubernetes",
                "applicationResources": {
                    "cpuPool": {
                        "numCPU": 1,
                        "memory": 1024,
                        "topology": {
                            "minNumberOfNodes": 1,
                            "minNodeCpu": 1,
                            "minNodeMemory": 512,
                        },
                    }
                },
                "isStandalone": True,
                "version": "1.28",
            },
            "componentSpec": [
                {
                    "componentName": "aeros-component",
                    "networkInterfaces": [
                        {
                            "interfaceId": "eth0",
                            "protocol": "TCP",
                            "port": 9090,
                            "visibilityType": "VISIBILITY_INTERNAL",
                        }
                    ],
                }
            ],
        },
        "APP_ID": "aeros-app-2",
        "APP_ZONES": [
            {
                "kubernetesClusterRef": "not-used",
                "EdgeCloudZone": {
                    "edgeCloudZoneId": "urn:ngsi-ld:Domain:NCSRD",
                    "edgeCloudZoneName": "not-used",
                    "edgeCloudZoneStatus": "not-used",
                    "edgeCloudProvider": "not-used",
                    "edgeCloudRegion": "not-used",
                },
            }
        ],
    },
}
