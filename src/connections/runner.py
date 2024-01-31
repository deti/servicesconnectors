""" Connector runner """

from src.connections.connectors.appstore import AppstoreConnector
from src.connections.models import Connection
from src.connections.storage import Storage


class RunnerException(Exception):
    """Runner exception"""


def run_connector(connector: Connection):
    """Run a connector"""
    storage = Storage()

    connector_class = None
    if connector.type == "appstore":
        connector_class = AppstoreConnector

    if connector_class is None:
        raise RunnerException(f"Connector {connector.type} not found")

    connector_executor = connector_class(connector)
    data = connector_executor.read_source()

    storage.write(data, connector.uuid)  # type: ignore
