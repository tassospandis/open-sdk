```mermaid
sequenceDiagram
title Retrieve Edge Cloud Zones (i2Edge EdgeCloud Platform)
actor AP as App Vertical Provider
participant CE as Capabilities Exposure
box Service Resource Manager
    participant API
    participant SDK as EdgeCloudSDK
end
participant i2Edge

AP ->> CE: GET /edge-cloud-zones
CE ->> API: GET /av. zones
API ->> SDK: sdk.i2edge.get_zones()
    
SDK ->> i2Edge: GET /zones/list
```