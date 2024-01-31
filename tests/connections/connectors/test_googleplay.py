from src.connections.connectors.connector import Connector
from src.connections.connectors.googleplay import GooglePlayConnector
from tests.connections.fakes import fake_connection


def test_googleplay_inherits_from_connector():
    """Test GooglePlayConnector inherits from Connector"""

    connection = fake_connection()
    connector = GooglePlayConnector(connection)

    assert isinstance(connector, Connector)
