""" Connector runner """

from src.connectors.connectors.appstore import AppstoreConnector
from src.connectors.models import Connector
from src.connectors.storage import Storage


class RunnerException(Exception):
    """Runner exception"""


def run_connector(connector: Connector):
    """Run a connector"""
    storage = Storage()

    connector_class = None
    if connector.connector_type == "appstore":
        connector_class = AppstoreConnector

    if connector_class is None:
        raise RunnerException(f"Connector {connector.connector_type} not found")

    connector_executor = connector_class(connector)
    data = connector_executor.read_source()

    storage.write(data, connector.uuid)  # type: ignore
