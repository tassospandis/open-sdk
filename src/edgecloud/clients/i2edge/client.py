#!/usr/bin/env python3
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
from typing import Dict, List, Optional

from src import logger
from src.edgecloud.core.edgecloud_interface import EdgeCloudManagementInterface

from . import schemas
from .common import (
    I2EdgeError,
    i2edge_delete,
    i2edge_get,
    i2edge_post,
    i2edge_post_multiform_data,
)


class EdgeApplicationManager(EdgeCloudManagementInterface):
    def __init__(self, base_url: str):
        self.base_url = base_url

    def get_edge_cloud_zones(
        self, region: Optional[str] = None, status: Optional[str] = None
    ) -> list[dict]:
        # Note: status is not supported by i2Edge; won't be used
        # Up to now; region == av_zone (so if region is specified, that zone will be returned)
        try:
            params = {}
            if region is not None:
                url = "{}/zone/{}".format(self.base_url, region)
                if status is not None:
                    params["status"] = status
                response = i2edge_get(url, params=params)
            else:
                url = "{}/zones/list".format(self.base_url)
                if status is not None:
                    params["status"] = status
                response = i2edge_get(url, params=params)

            return response
        except I2EdgeError as e:
            raise e

    def _create_artefact(
        self,
        artefact_id: str,
        artefact_name: str,
        repo_name: str,
        repo_type: str,
        repo_url: str,
        password: Optional[str] = None,
        token: Optional[str] = None,
        user_name: Optional[str] = None,
    ):
        repo_type = schemas.RepoType(repo_type)
        url = "{}/artefact".format(self.base_url)
        payload = schemas.ArtefactOnboarding(
            artefact_id=artefact_id,
            name=artefact_name,
            repo_password=password,
            repo_name=repo_name,
            repo_type=repo_type,
            repo_url=repo_url,
            repo_token=token,
            repo_user_name=user_name,
        )
        try:
            i2edge_post_multiform_data(url, payload)
        except I2EdgeError as e:
            raise e

    def _get_artefact(self, artefact_id: str) -> Dict:
        url = "{}/artefact/{}".format(self.base_url, artefact_id)
        try:
            response = i2edge_get(url, artefact_id)
            return response
        except I2EdgeError as e:
            raise e

    def _get_all_artefacts(self) -> List[Dict]:
        url = "{}/artefact".format(self.base_url)
        try:
            response = i2edge_get(url, {})
            return response
        except I2EdgeError as e:
            raise

    def _delete_artefact(self, artefact_id: str):
        url = "{}/artefact".format(self.base_url)
        try:
            i2edge_delete(url, artefact_id)
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
