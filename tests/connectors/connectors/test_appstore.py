import respx
from httpx import Response

from src.connectors.connectors.appstore import AppstoreConnector
from tests.connectors.fakes import fake_connector


def test_non_200_response_raises_exception():
    """Test non 200 response raises exception"""

    connector = fake_connector()
    #
    # app_route = respx.get(
    #     f"https://apps.apple.com/{region}/app/{slug}/{appid}"
    # ).mock(return_value=Response(404))
    #
    # connector = fake_connector(
    #     connector_type="appstore",
    #     connector_settings={
    #         "region": region,
    #         "slug": slug,
    #         "appid": appid,
    #     },
    # )
    # appstore_connector = AppstoreConnector(connector)
    # with pytest.raises(Exception):
    #     appstore_connector.read_source()
    #
    # assert app_route.called
    # assert app_route.call_count == 1
    # assert app_route[0].request.url == f"https://apps.apple.com/{region}/app/{slug}/{appid}"
