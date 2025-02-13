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
from typing import Optional

from .. import logger

from . import schemas
from .common import I2EdgeError, i2edge_delete, i2edge_get, i2edge_post, i2edge_post_multiform_data

log = logger.get_logger(__name__)

# TODO: Extend EdgeApplicationManagementInterface(ABC)
class I2EdgeClient:
    def __init__(self, i2edge_base_url: str):
        self.base_url = i2edge_base_url

    def deploy_app(
        self,
        appId: str,
        zoneId: str,
        flavourId: str,
        namespace: str,
        appProviderId: Optional[str] = None,
        appVersion: Optional[str] = None,
    ):
        app_provider_id = "" if appProviderId is None else appProviderId
        app_version = "" if appVersion is None else appVersion
        app_deploy_data = schemas.AppDeployData(
            appId=appId,
            appProviderId=app_provider_id,
            appVersion=app_version,
            zoneInfo=schemas.ZoneInfo(flavourId=flavourId, zoneId=zoneId),
        )
        app_parameters = schemas.AppParameters(namespace=namespace)
        url = "{}/app/".format(self.base_url)
        payload = schemas.AppDeploy(app_deploy_data=app_deploy_data, app_parameters=app_parameters)
        try:
            i2edge_post(url, payload)  # TODO Think if we care about the response. So far we don't
            log.info("App deployed successfully")
            return namespace
        except I2EdgeError as e:
            raise e

    def undeploy_app(self, app_name):
        url = "{}/app".format(self.base_url)
        try:
            i2edge_delete(url, app_name)
            log.info("App undeployed successfully")
        except I2EdgeError as e:
            raise e

    def create_artefact(
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
            # chart=None,  # XXX AFAIK not supported by CAMARA.
            repo_password=password,
            repo_name=repo_name,
            repo_type=repo_type,
            repo_url=repo_url,
            repo_token=token,
            repo_user_name=user_name,
        )
        try:
            i2edge_post_multiform_data(url, payload)
            log.info("Artefact created successfully")
        except I2EdgeError as e:
            raise e

    def delete_artefact(self, artefact_id: str):
        url = "{}/artefact".format(self.base_url)
        try:
            i2edge_delete(url, artefact_id)
            log.info("Artefact deleted successfully")
        except I2EdgeError as e:
            raise e

    def onboard_app(self, app_id: str, artefact_id: str):
        app_component_spec = schemas.AppComponentSpec(artefactId=artefact_id)
        # TODO Why passing a list of app_component_specs? AFAIK i2edge only accepts one artifact at time.
        data = schemas.ApplicationOnboardingData(
            app_id=app_id, appComponentSpecs=[app_component_spec]
        )
        payload = schemas.ApplicationOnboardingRequest(profile_data=data)
        url = "{}/application/onboarding".format(self.base_url)
        try:
            i2edge_post(url, payload)
            log.info("App onboarded successfully")
        except I2EdgeError as e:
            raise e

    def get_all_onboarded_apps(self) -> list[dict]:
        # TODO
        pass

    def delete_onboarded_app(self, app_id: str):
        url = "{}/application/onboarding".format(self.base_url)
        try:
            i2edge_delete(url, app_id)
            log.info("App deleted successfully")
        except I2EdgeError as e:
            raise e

    def create_flavour(
        self,
        zone_id: str,
        memory_size: str,
        num_cpu: int,
        num_gpus: Optional[int] = None,
    ) -> str:
        url = "{}/zone/{}/flavour".format(self.base_url, zone_id)
        gpu_list = [schemas.GPU(numGPU=num_gpus)] if num_gpus is not None else None
        flavour_data = schemas.Flavour(
            flavour_supported=schemas.FlavourSupported(
                memorySize=memory_size, numCPU=num_cpu, gpu=gpu_list
            )
        )
        try:
            response = i2edge_post(url, flavour_data)
            log.info("Flavour created successfully")
            id_value = response['response'].split('id ')[1].split(' ')[0]
            return id_value
        except I2EdgeError as e:
            raise e

    def delete_flavour(self, zone_id: str, flavour_id: str):
        url = "{}/zone/{}/flavour".format(self.base_url, zone_id)
        try:
            i2edge_delete(url, flavour_id)
            log.info("Flavour deleted successfully")
        except I2EdgeError as e:
            raise e

    def get_all_deployed_apps(self) -> list[dict]:
        url = "{}/app".format(self.base_url)
        try:
            response = i2edge_get(url, params=None)
            return response
        except I2EdgeError as e:
            raise e

    def get_edge_cloud_zones(self) -> list[dict]:
        url = "{}/zones/list".format(self.base_url)
        try:
            response = i2edge_get(url, params=None)
            return response
        except I2EdgeError as e:
            raise e
