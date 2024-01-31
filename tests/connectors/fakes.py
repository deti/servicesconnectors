import json

from faker import Faker

from src.connectors.models import Connector

fake = Faker()


def fake_appstore_connector_settings() -> dict:
    return {
        "region": fake.country_code().lower(),
        "slug": fake.slug(),
        "appid": f"id{fake.random_int()}",
    }


def fake_connector() -> Connector:
    connector_settings = fake_appstore_connector_settings()
    return Connector(
        uuid=fake.uuid4(),
        connector_type=fake.word(),
        connector_settings=json.dumps(connector_settings),
        description=fake.sentence(),
    )
