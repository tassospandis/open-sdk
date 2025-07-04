# coding: utf-8

from __future__ import absolute_import

from datetime import date, datetime  # noqa: F401
from typing import Dict, List  # noqa: F401

from sunrise6g_opensdk.edgecloud.adapters.kubernetes.lib import util
from sunrise6g_opensdk.edgecloud.adapters.kubernetes.lib.models.base_model_ import Model


class NodesResponse(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    def __init__(
        self,
        id: str = None,
        name: str = None,
        location: str = None,
        serial: str = None,
        node_type: str = None,
        status: str = None,
    ):  # noqa: E501
        """NodesResponse - a model defined in Swagger

        :param id: The id of this NodesResponse.  # noqa: E501
        :type id: str
        :param name: The name of this NodesResponse.  # noqa: E501
        :type name: str
        :param location: The location of this NodesResponse.  # noqa: E501
        :type location: str
        :param serial: The serial of this NodesResponse.  # noqa: E501
        :type serial: str
        :param node_type: The node_type of this NodesResponse.  # noqa: E501
        :type node_type: str
        """
        self.swagger_types = {
            "id": str,
            "name": str,
            "location": str,
            "serial": str,
            "node_type": str,
            "status": str,
        }

        self.attribute_map = {
            "id": "id",
            "name": "name",
            "location": "location",
            "serial": "serial",
            "node_type": "node_type",
            "status": "status",
        }
        self._id = id
        self._name = name
        self._location = location
        self._serial = serial
        self._node_type = node_type
        self._status = status

    @classmethod
    def from_dict(cls, dikt) -> "NodesResponse":
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The nodesResponse of this NodesResponse.  # noqa: E501
        :rtype: NodesResponse
        """
        return util.deserialize_model(dikt, cls)

    @property
    def id(self) -> str:
        """Gets the id of this NodesResponse.


        :return: The id of this NodesResponse.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id: str):
        """Sets the id of this NodesResponse.


        :param id: The id of this NodesResponse.
        :type id: str
        """

        self._id = id

    @property
    def name(self) -> str:
        """Gets the name of this NodesResponse.


        :return: The name of this NodesResponse.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name: str):
        """Sets the name of this NodesResponse.


        :param name: The name of this NodesResponse.
        :type name: str
        """

        self._name = name

    @property
    def location(self) -> str:
        """Gets the location of this NodesResponse.


        :return: The location of this NodesResponse.
        :rtype: str
        """
        return self._location

    @location.setter
    def location(self, location: str):
        """Sets the location of this NodesResponse.


        :param location: The location of this NodesResponse.
        :type location: str
        """

        self._location = location

    @property
    def serial(self) -> str:
        """Gets the serial of this NodesResponse.


        :return: The serial of this NodesResponse.
        :rtype: str
        """
        return self._serial

    @serial.setter
    def serial(self, serial: str):
        """Sets the serial of this NodesResponse.


        :param serial: The serial of this NodesResponse.
        :type serial: str
        """

        self._serial = serial

    @property
    def node_type(self) -> str:
        """Gets the node_type of this NodesResponse.


        :return: The node_type of this NodesResponse.
        :rtype: str
        """
        return self._node_type

    @node_type.setter
    def node_type(self, node_type: str):
        """Sets the node_type of this NodesResponse.


        :param node_type: The node_type of this NodesResponse.
        :type node_type: str
        """

        self._node_type = node_type

    @property
    def status(self) -> str:
        """Gets the node_type of this NodesResponse.


        :return: The node_type of this NodesResponse.
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status: str):
        """Sets the node_type of this NodesResponse.


        :param node_type: The node_type of this NodesResponse.
        :type node_type: str
        """

        self._status = status
