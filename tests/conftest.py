""" Pytest configuration file. """

from pathlib import Path
from typing import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from alembic import command
from alembic.config import Config
from src.database import engine
from src.main import app

ROOT_PATH = Path(__file__).parent.parent


@pytest.fixture(scope="function")
def db() -> Generator:
    # Configure your Alembic Config for testing
    alembic_cfg = Config(ROOT_PATH / "alembic.ini")
    alembic_cfg.set_main_option("script_location", str(ROOT_PATH / "src/alembic"))

    # Apply migrations
    command.upgrade(alembic_cfg, "head")

    with Session(engine) as session:
        yield session

    # Downgrade migrations
    command.downgrade(alembic_cfg, "base")


@pytest.fixture(scope="module")
def client() -> Generator:
    """Test client fixture"""
    with TestClient(app) as c:
        yield c
