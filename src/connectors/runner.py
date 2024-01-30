""" Connector runner """

from src.connectors.connectors.appstore import AppstoreConnector
from src.connectors.models import Connector
from src.connectors.storage import Storage


class RunnerException(Exception):
    """Runner exception"""


def connector_runner(connector: Connector):
    """Run a connector"""
    storage = Storage()

    connector_class = None
    if connector.connector_type == "appstore":
        connector_class = AppstoreConnector

    if connector_class is None:
        raise RunnerException(f"Connector {connector.connector_settings} not found")

    connector_executor = connector_class(storage, connector)
    connector_executor.syncronize()
