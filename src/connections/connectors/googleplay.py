""" Google play connections module """

from .abstractconnector import Connector


class GooglePlayConnector(Connector):
    """Google play connector"""

    def read_source(self) -> dict:
        """Read data from google play connections"""
        return {"data": "data"}
