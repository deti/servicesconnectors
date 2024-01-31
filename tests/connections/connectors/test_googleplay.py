import json
from unittest.mock import ANY, call, patch

import pytest
import respx
from httpx import Response

from src.connections.connectors.connector import Connector, ConnectorException
from src.connections.connectors.googleplay import (
    GooglePlayConnector, GooglePlayConnectorException)
from tests.connections.fakes import fake_connection


def test_googleplay_exception_inherits_from_connector_exception():
    """Test GooglePlayConnectorException inherits from ConnectorException"""

    exception = GooglePlayConnectorException("test", {})
    assert isinstance(exception, ConnectorException)


def test_googleplay_inherits_from_connector():
    """Test GooglePlayConnector inherits from Connector"""

    connection = fake_connection()
    connector = GooglePlayConnector(connection)

    assert isinstance(connector, Connector)


@respx.mock
def test_non_200_response_raises_exception():
    """Test non 200 response raises exception"""

    connection = fake_connection()
    settings = json.loads(connection.settings)
    connector = GooglePlayConnector(connection)

    app_route = respx.get(
        f"https://play.google.com/store/apps/details?id={settings['slug']}"
    ).mock(return_value=Response(404))

    with pytest.raises(GooglePlayConnectorException):
        connector.read_source()

    assert app_route.called
    assert app_route.call_count == 1


@respx.mock
def test_200_response_returns_googleplay_item():
    """Test 200 response returns googleplay item"""

    connection = fake_connection()
    settings = json.loads(connection.settings)
    connector = GooglePlayConnector(connection)

    googleplay_url = f"https://play.google.com/store/apps/details?id={settings['slug']}"

    app_route = respx.get(googleplay_url).mock(
        return_value=Response(
            status_code=200, text="<html><body><h1>mocked text</h1></body></html>"
        )
    )

    with (
        patch(
            "src.connections.connectors.googleplay.get_element_text"
        ) as mock_get_element_text,
        patch(
            "src.connections.connectors.googleplay.get_all_element_text"
        ) as mock_get_all_element_text,
    ):
        mock_get_element_text.return_value = "mocked text"
        mock_get_all_element_text.return_value = ["mocked reviews"]
        assert connector.read_source() == {
            "url": googleplay_url,
            "itemtype": "googleplay",
            "name": "mocked text",
            "description": "mocked text",
            "rating": "mocked text",
            "reviews": ["mocked reviews"],
        }

        mock_get_element_text.assert_has_calls(
            [
                call(ANY, "h1", {"itemprop": "name"}),
                call(ANY, "div", {"data-g-id": "description"}),
                call(ANY, "div", {"itemprop": "starRating"}),
            ]
        )
        mock_get_all_element_text.assert_called_once_with(ANY, "div", class_="h3YV2d")

    assert app_route.called
    assert app_route.call_count == 1
