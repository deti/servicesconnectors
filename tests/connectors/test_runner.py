from unittest.mock import patch

import pytest

from src.connectors.runner import RunnerException, run_connector
from tests.connectors.fakes import fake_connector


def test_run_connector_raises_on_unknown_connector():
    """Test run connector raises on unknown connector"""
    connector = fake_connector()
    connector.connector_type = "unknown"

    with pytest.raises(RunnerException) as excinfo:
        run_connector(connector)
        assert "Connector unknown not found" in str(excinfo.value)


def test_run_connector_executes_appsotre_connector():
    """Test run connector executes appstore connector"""
    connector = fake_connector()
    connector.connector_type = "appstore"

    expected_data = {"test": "test"}

    with (
        patch("src.connectors.runner.Storage") as mock_storage,
        patch("src.connectors.runner.AppstoreConnector") as mock_appstore_connector,
    ):
        mock_storage().write.return_value = None
        mock_appstore_connector().read_source.return_value = expected_data
        run_connector(connector)

        mock_appstore_connector.assert_called_with(connector)
        mock_appstore_connector().read_source.assert_called_once()
        mock_storage().write.assert_called_once_with(expected_data, connector.uuid)
