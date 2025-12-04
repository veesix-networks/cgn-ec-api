from secrets import choice

import pytest
from httpx import AsyncClient

from cgn_ec_api.models.metrics import (
    NATPortBlockMapping,
)


@pytest.mark.asyncio
async def test_api_v1_port_block_mappings_get(async_test_app: AsyncClient):
    response = await async_test_app.get("/v1/port_block_mappings/")
    data = response.json()
    assert len(data) >= 1


@pytest.mark.asyncio
async def test_api_v1_port_block_mappings_get_params_limit(async_test_app: AsyncClient):
    params = {"limit": 10}
    response = await async_test_app.get("/v1/port_block_mappings/", params=params)
    data = response.json()
    assert len(data) == 10


@pytest.mark.asyncio
async def test_api_v1_port_block_mappings_get_params_skip(async_test_app: AsyncClient):
    params = {"limit": 10}
    response1 = await async_test_app.get("/v1/port_block_mappings/", params=params)
    data1 = response1.json()

    params["skip"] = 10
    response2 = await async_test_app.get("/v1/port_block_mappings/", params=params)
    data2 = response2.json()

    assert data1 != data2


@pytest.mark.asyncio
async def test_api_v1_port_block_mappings_get_params_x_ip(
    async_test_app: AsyncClient,
    generate_port_block_mapping_metrics: list[NATPortBlockMapping],
):
    record = choice(generate_port_block_mapping_metrics)

    params = {"x_ip": record.x_ip}
    response = await async_test_app.get("/v1/port_block_mappings/", params=params)
    data = response.json()

    for session in data:
        assert session["x_ip"] == record.x_ip


@pytest.mark.asyncio
async def test_api_v1_port_block_mappings_get_params_start_port(
    async_test_app: AsyncClient,
    generate_port_block_mapping_metrics: list[NATPortBlockMapping],
):
    record = choice(generate_port_block_mapping_metrics)

    params = {"start_port": record.start_port}
    response = await async_test_app.get("/v1/port_block_mappings/", params=params)
    data = response.json()

    for session in data:
        assert session["start_port"] == record.start_port


@pytest.mark.asyncio
async def test_api_v1_port_block_mappings_get_params_end_port(
    async_test_app: AsyncClient,
    generate_port_block_mapping_metrics: list[NATPortBlockMapping],
):
    record = choice(generate_port_block_mapping_metrics)

    params = {"end_port": record.end_port}
    response = await async_test_app.get("/v1/port_block_mappings/", params=params)
    data = response.json()

    for session in data:
        assert session["end_port"] == record.end_port


@pytest.mark.asyncio
async def test_api_v1_port_block_mappings_get_params_port(
    async_test_app: AsyncClient,
    generate_port_block_mapping_metrics: list[NATPortBlockMapping],
):
    record = choice(generate_port_block_mapping_metrics)
    port = (record.start_port + record.end_port) // 2

    params = {"port": port}
    response = await async_test_app.get("/v1/port_block_mappings/", params=params)
    data = response.json()

    assert len(data) >= 1
    for mapping in data:
        assert mapping["start_port"] <= port <= mapping["end_port"]
