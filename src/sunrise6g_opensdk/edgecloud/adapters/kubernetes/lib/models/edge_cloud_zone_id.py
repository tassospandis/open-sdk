# coding: utf-8

from __future__ import absolute_import

from datetime import date, datetime  # noqa: F401
from typing import Dict, List  # noqa: F401

from sunrise6g_opensdk.edgecloud.adapters.kubernetes.lib import util
from sunrise6g_opensdk.edgecloud.adapters.kubernetes.lib.models.base_model_ import Model


class EdgeCloudZoneId(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    def __init__(self):  # noqa: E501
        """EdgeCloudZoneId - a model defined in Swagger"""
        self.swagger_types = {}

        self.attribute_map = {}

    @classmethod
    def from_dict(cls, dikt) -> "EdgeCloudZoneId":
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The EdgeCloudZoneId of this EdgeCloudZoneId.  # noqa: E501
        :rtype: EdgeCloudZoneId
        """
        return util.deserialize_model(dikt, cls)
