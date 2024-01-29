""" Pytest configuration file. """

from typing import Generator

import pytest
from fastapi.testclient import TestClient

from src.main import app


@pytest.fixture(scope="module")
def client() -> Generator:
    """Test client fixture"""
    with TestClient(app) as c:
        yield c
