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
#   - Adrián Pino Martínez (adrian.pino@i2cat.net)
#   - Sergio Giménez (sergio.gimenez@i2cat.net)
##
from typing import Optional
from src.edgecloud.core.edgecloud_interface import EdgeCloudManagementInterface
from typing import Dict, List, Optional
from . import schemas
from .common import I2EdgeError, i2edge_delete, i2edge_get, i2edge_post, i2edge_post_multiform_data

class EdgeApplicationManager(EdgeCloudManagementInterface):
    def __init__(self, base_url: str):
        self.base_url = base_url

    def get_edge_cloud_zones(self, region: Optional[str] = None, status: Optional[str] = None) -> list[dict]:
        # Note: status is not supported by i2Edge; won't be used
        try:
            params = {}
            if region is not None:
                # Use the /zone/{region} endpoint
                url = "{}/zone/{}".format(self.base_url, region)
                if status is not None:
                    params['status'] = status
                response = i2edge_get(url, params=params)
            else:
                # Use the /zones/list endpoint
                url = "{}/zones/list".format(self.base_url)
                if status is not None:
                    params['status'] = status
                response = i2edge_get(url, params=params)
            
            return response
        except I2EdgeError as e:
            raise e

        try:
            response = i2edge_get(url, params=None)
            return response
        except I2EdgeError as e:
            raise e

    def onboard_app(self, app_manifest: Dict) -> Dict:
        print(f"Submitting application: {app_manifest}")
        return {"appId": "1234-5678"}

    def get_all_onboarded_apps(self) -> List[Dict]:
        return [{"appId": "1234-5678", "name": "TestApp"}]

    def get_onboarded_app(self, app_id: str) -> Dict:
        return {"appId": app_id, "name": "TestApp"}

    def delete_onboarded_app(self, app_id: str) -> None:
        print(f"Deleting application: {app_id}")

    def deploy_app(self, app_id: str, app_zones: List[Dict]) -> Dict:
        return {"appInstanceId": "abcd-efgh"}

    def get_all_deployed_apps(self, app_id: Optional[str] = None, app_instance_id: Optional[str] = None, region: Optional[str] = None) -> List[Dict]:
        return [{"appInstanceId": "abcd-efgh", "status": "ready"}]

    def undeploy_app(self, app_instance_id: str) -> None:
        print(f"Deleting app instance: {app_instance_id}")
