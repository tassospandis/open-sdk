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
ARTEFACT_ID = "aeros-id-1"
ARTEFACT_NAME = "i2edgechart"
REPO_NAME = "github-cesar"
REPO_TYPE = "PUBLICREPO"
REPO_URL = "https://cesarcajas.github.io/helm-charts-examples/"

# Onboarding: CAMARA /app payload (only mandatory fields)
APP_ONBOARD_MANIFEST = {
    "appId": ARTEFACT_ID,
    "name": "aeros-SDK",
    "version": "1.0.0",
    "appProvider": "ncsrd",
    "packageType": "CONTAINER",
    "appRepo": {
        "type": "PUBLICREPO",
        "imagePath": "https://example.com/nginx:latest",
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
AEROS_APP_ID = "urn:ngsi-ld:Service:sunriseapp2"
AEROS_TOSCA_DESCRIPTOR = {
    "serviceId": AEROS_APP_ID,
    "tosca": """
  tosca_definitions_version: tosca_simple_yaml_1_3
  description: TOSCA for network performance
  node_templates:
    influxdb:
      type: tosca.nodes.Container.Application
      requirements:
        - network:
            properties:
              ports:
                fastapi:
                  properties:
                    protocol: [tcp]
                    source: 8086
              exposePorts: true
        - host:
            node_filter:
              properties:
                id: "urn:ngsi-ld:InfrastructureElement:NCSRD:cebf2bd4d0ba"
      artifacts:
        influxdb-image:
          file: p4lik4ri/influxdb
          type: tosca.artifacts.Deployment.Image.Container.Docker
          repository: docker_hub
      interfaces:
        Standard:
          create:
            implementation: influxdb-image
            inputs:
              envVars:
                - INFLUXDB_BUCKET: some-bucket
                - INFLUXDB_ORG: NCSRD
                - INFLUXDB_USER: vpitsilis
                - INFLUXDB_USER_PASSWORD: mypassword
  """,
}

AEROS_ZONE_ID = "urn:ngsi-ld:Domain:NCSRD"

AEROS_TOSCA_DESCRIPTOR_2 = """
tosca_definitions_version: tosca_simple_yaml_1_3
description: A test service for testing TOSCA generation
node_templates:
  auto-component:
    artifacts:
      nginx-image:
        file: nginx
        type: tosca.artifacts.Deployment.Image.Container.Docker
        repository: docker_hub
    interfaces:
      Standard:
        create:
          implementation: application_image
          inputs:
            cliArgs: []
            envVars: []
    requirements:
    - network:
        properties:
          ports:
            port1:
              properties:
                protocol:
                - tcp
                source: 80
            port2:
              properties:
                protocol:
                - tcp
                source: 443
          exposePorts: false
    - host:
        node_filter:
          capabilities:
          - host:
              properties:
                cpu_arch:
                  equal: x64
                realtime:
                  equal: false
                cpu_usage:
                  less_or_equal: '0.4'
                mem_size:
                  greater_or_equal: '1'
                energy_efficiency:
                  greater_or_equal: '10'
                green:
                  greater_or_equal: '10'
          properties: null
    type: tosca.nodes.Container.Application
"""
