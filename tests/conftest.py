import asyncio
from typing import Generator, AsyncGenerator

import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from httpx import AsyncClient, ASGITransport
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import async_sessionmaker
from testcontainers.postgres import PostgresContainer

from cgn_ec_api.config import settings
from cgn_ec_api.main import app
from cgn_ec_api.dependencies.database import get_engine, get_db
from cgn_ec_api.models.metrics import (
    NATAddressMapping,
    NATPortBlockMapping,
    NATPortMapping,
    NATSessionMapping,
)

pytest_plugins = ["tests.fixtures.metrics"]

postgres = PostgresContainer(
    "postgres:17-alpine",
    username=settings.POSTGRES_USER,
    password=settings.POSTGRES_PASSWORD,
    dbname=settings.POSTGRES_DB,
    driver="postgresql+psycopg",
)


@pytest.fixture(scope="session", autouse=True)
def setup(request):
    postgres.start()

    def remove_container():
        postgres.stop()

    request.addfinalizer(remove_container)


@pytest.fixture(scope="module")
def test_app():
    client = TestClient(app)
    yield client


@pytest_asyncio.fixture(scope="module")
async def async_test_app(async_session: AsyncSession):
    async def override_get_db() -> AsyncGenerator[AsyncSession, None]:
        yield async_session

    app.dependency_overrides[get_db] = override_get_db

    transport = ASGITransport(app=app)
    async with AsyncClient(
        transport=transport,
        base_url="http://test",
        headers={settings.API_KEY_HEADER: settings.API_KEYS[0]},
    ) as client:
        yield client


@pytest.fixture(scope="session")
def event_loop(request) -> Generator:
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session")
async def async_session(
    generate_session_mapping_metrics: list[NATSessionMapping],
    generate_address_mapping_metrics: list[NATAddressMapping],
    generate_port_mapping_metrics: list[NATPortMapping],
    generate_port_block_mapping_metrics: list[NATPortBlockMapping],
) -> AsyncSession:
    test_engine = get_engine(
        f"postgresql+psycopg://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@localhost:{postgres.get_exposed_port(settings.POSTGRES_PORT)}/{settings.POSTGRES_DB}",
    )

    async_test_session = async_sessionmaker(
        test_engine, class_=AsyncSession, expire_on_commit=False
    )

    async with async_test_session() as s:
        async with test_engine.begin() as conn:
            await conn.run_sync(
                SQLModel.metadata.create_all,
                tables=[
                    NATSessionMapping.__table__,
                    NATAddressMapping.__table__,
                    NATPortMapping.__table__,
                    NATPortBlockMapping.__table__,
                ],
            )

        metrics = (
            generate_session_mapping_metrics
            + generate_address_mapping_metrics
            + generate_port_mapping_metrics
            + generate_port_block_mapping_metrics
        )
        await insert_test_data(s, metrics)
        yield s

    async with test_engine.begin() as conn:
        await conn.run_sync(
            SQLModel.metadata.drop_all,
            tables=[
                NATSessionMapping.__table__,
                NATAddressMapping.__table__,
                NATPortMapping.__table__,
                NATPortBlockMapping.__table__,
            ],
        )

    await test_engine.dispose()


async def insert_test_data(session: AsyncSession, metrics: list[dict]):
    """Insert initial test data."""
    for item in metrics:
        session.add(item)

    await session.commit()
