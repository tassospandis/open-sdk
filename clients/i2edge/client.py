#!/usr/bin/env python3
# -*- coding: utf-8 -*-
##
# Copyright 2025-present by Software Networks Area, i2CAT.
# All rights reserved.
#
# This file is part of the Federation SDK
# Unauthorized copying of this file, via any medium is strictly prohibited.
#
# Contributors:
#   - Sergio Giménez (sergio.gimenez@i2cat.net)
#   - Adrián Pino (adrian.pino@i2cat.net)
##
from typing import Dict, List, Optional
from edgecloud_interface import EdgeApplicationManagementInterface

class EdgeApplicationManager(EdgeApplicationManagementInterface):
    def onboard_app(self, app_manifest: Dict) -> Dict:
        print(f"Submitting application: {app_manifest}")
        return {"appId": "1234-5678"}

    def get_onboarded_apps(self) -> List[Dict]:
        return [{"appId": "1234-5678", "name": "TestApp"}]

    def get_onboarded_app(self, app_id: str) -> Dict:
        return {"appId": app_id, "name": "TestApp"}

    def delete_onboarded_app(self, app_id: str) -> None:
        print(f"Deleting application: {app_id}")

    def create_app_instance(self, app_id: str, app_zones: List[Dict]) -> Dict:
        return {"appInstanceId": "abcd-efgh"}

    def get_app_instances(self, app_id: Optional[str] = None, app_instance_id: Optional[str] = None, region: Optional[str] = None) -> List[Dict]:
        return [{"appInstanceId": "abcd-efgh", "status": "ready"}]

    def delete_app_instance(self, app_instance_id: str) -> None:
        print(f"Deleting app instance: {app_instance_id}")

    def get_edge_cloud_zones(self, region: Optional[str] = None, status: Optional[str] = None) -> List[Dict]:
        return [{"edgeCloudZoneId": "zone-1", "status": "active"}]
    