""" Connector runner """

from src.connections.connectors.appstore import AppstoreConnector
from src.connections.models import Connection
from src.connections.storage import Storage


class RunnerException(Exception):
    """Runner exception"""


def run_connector(connection: Connection):
    """Run a connector"""
    storage = Storage()

    connector_class = None
    if connection.type == "appstore":
        connector_class = AppstoreConnector

    if connector_class is None:
        raise RunnerException(f"Connector {connection.type} not found")

    connector = connector_class(connection)
    data = connector.read_source()

    storage.write(data, connection.uuid)  # type: ignore
