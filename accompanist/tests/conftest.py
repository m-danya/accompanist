import json
from datetime import datetime

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy import insert

from accompanist.collection.models import Album, Artist, Track
from accompanist.config import settings
from accompanist.database import Base, async_session_maker, engine
from accompanist.main import app as fastapi_app

# supports datetimes copied from dbeaver
TEST_DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"


@pytest.fixture(scope="session")
def test_data():
    with open("accompanist/tests/data.json") as f:
        test_data = json.load(f)
    for table_key in test_data:
        for row in test_data[table_key]:
            for column in row:
                if column.endswith("_at"):
                    row[column] = datetime.strptime(row[column], TEST_DATETIME_FORMAT)
    test_data["albums"].sort(key=lambda x: x["id"])
    test_data["tracks"].sort(key=lambda x: x["id"])
    # TODO: make this dict immutable to prevent accidental modification
    return test_data


@pytest.fixture(scope="session")
def test_album_data(test_data):
    return test_data["albums"]


@pytest.fixture(scope="session")
def test_track_data(test_data):
    return test_data["tracks"]


@pytest.fixture(scope="function", autouse=True)
async def prepare_database(test_data):
    assert settings.MODE == "TEST"
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    async with async_session_maker() as session:
        for Model, table_key in [
            (Artist, "artists"),
            (Album, "albums"),
            (Track, "tracks"),
        ]:
            query = insert(Model).values(test_data[table_key])
            await session.execute(query)

        await session.commit()


@pytest.fixture(scope="function")
async def ac():
    async with AsyncClient(
        transport=ASGITransport(app=fastapi_app), base_url="http://test"
    ) as ac:
        yield ac
