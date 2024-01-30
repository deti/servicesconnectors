from faker import Faker

from src.connectors.models import Connector

fake = Faker()


def fake_connector() -> Connector:
    return Connector(
        uuid=fake.uuid4(),
        connector_type=fake.word(),
        connector_settings=fake.json(),
        description=fake.sentence(),
    )
