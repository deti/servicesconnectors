import json

from faker import Faker

from src.connections.models import Connection

fake = Faker()


def fake_appstore_settings() -> dict:
    return {
        "region": fake.country_code().lower(),
        "slug": fake.slug(),
        "appid": f"id{fake.random_int()}",
    }


def fake_connection() -> Connection:
    settings = fake_appstore_settings()
    return Connection(
        uuid=fake.uuid4(),
        type=fake.word(),
        settings=json.dumps(settings),
        description=fake.sentence(),
    )
