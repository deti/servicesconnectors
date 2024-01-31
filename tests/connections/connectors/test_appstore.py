import json
from unittest.mock import ANY, call, patch

import pytest
import respx
from httpx import Response

from src.connections.connectors.appstore import AppstoreConnector
from tests.connections.fakes import fake_connection


@respx.mock
def test_non_200_response_raises_exception():
    """Test non 200 response raises exception"""

    connector_model = fake_connection()
    settings = json.loads(connector_model.settings)
    appstore_connector = AppstoreConnector(connector_model)

    region = settings["region"]
    slug = settings["slug"]
    appid = settings["appid"]

    app_route = respx.get(f"https://apps.apple.com/{region}/app/{slug}/{appid}").mock(
        return_value=Response(404)
    )

    with pytest.raises(Exception):
        appstore_connector.read_source()

    assert app_route.called
    assert app_route.call_count == 1


@respx.mock
def test_200_response_returns_appstore_item():
    """Test 200 response returns appstore item"""

    connector_model = fake_connection()
    settings = json.loads(connector_model.settings)
    appstore_connector = AppstoreConnector(connector_model)

    region = settings["region"]
    slug = settings["slug"]
    appid = settings["appid"]
    appstore_url = f"https://apps.apple.com/{region}/app/{slug}/{appid}"

    app_route = respx.get(appstore_url).mock(
        return_value=Response(
            status_code=200, text="<html><body><h1>mocked text</h1></body></html>"
        )
    )

    reviews = ["mocked text 1", "mocked text 2"]

    with (
        patch(
            "src.connections.connectors.appstore.get_element_text"
        ) as mock_get_element_text,
        patch(
            "src.connections.connectors.appstore.get_all_element_text"
        ) as mock_get_all_element_text,
    ):
        mock_get_element_text.return_value = "mocked text"
        mock_get_all_element_text.return_value = reviews
        appstore_item = appstore_connector.read_source()

        # Assert parameters passed to get_element_text
        mock_get_element_text.assert_has_calls(
            [
                call(ANY, "h1", "product-header__title"),
                call(ANY, "h2", "product-header__subtitle"),
                call(ANY, "h2", "product-header__identity"),
                call(ANY, "li", "app-header__list__item--price"),
                call(ANY, "div", "section__description"),
                call(ANY, "div", "whats-new__content"),
                call(ANY, "span", "we-customer-ratings__averages__display"),
            ],
            any_order=True,
        )

        # Assert parameters passed to get_all_element_text
        mock_get_all_element_text.assert_called_with(ANY, "div", "we-customer-review")

    assert app_route.called
    assert app_route.call_count == 1

    assert appstore_item == {
        "item_uuid": connector_model.uuid,
        "type": "appstore",
        "url": appstore_url,
        "title": "mocked text",
        "subtitle": "mocked text",
        "company": "mocked text",
        "price": "mocked text",
        "description": "mocked text",
        "whats_new": "mocked text",
        "rating": "mocked text",
        "reviews": reviews,
    }
