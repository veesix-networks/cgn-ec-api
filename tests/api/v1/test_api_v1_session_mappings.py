from secrets import choice

import pytest
from httpx import AsyncClient

from cgn_ec_api.models.metrics import (
    NATSessionMapping,
)


@pytest.mark.asyncio
async def test_api_v1_session_mappings_get(async_test_app: AsyncClient):
    response = await async_test_app.get("/v1/session_mappings/")
    data = response.json()
    assert len(data) >= 1


@pytest.mark.asyncio
async def test_api_v1_session_mappings_get_params_limit(async_test_app: AsyncClient):
    params = {"limit": 10}
    response = await async_test_app.get("/v1/session_mappings/", params=params)
    data = response.json()
    assert len(data) == 10


@pytest.mark.asyncio
async def test_api_v1_session_mappings_get_params_skip(async_test_app: AsyncClient):
    params = {"limit": 10}
    response1 = await async_test_app.get("/v1/session_mappings/", params=params)
    data1 = response1.json()

    params["skip"] = 10
    response2 = await async_test_app.get("/v1/session_mappings/", params=params)
    data2 = response2.json()

    assert data1 != data2


@pytest.mark.asyncio
async def test_api_v1_session_mappings_get_params_protocol(async_test_app: AsyncClient):
    protocol = 6
    params = {"protocol": protocol}
    response = await async_test_app.get("/v1/session_mappings/", params=params)
    data = response.json()

    for session in data:
        assert session["protocol"] == protocol


@pytest.mark.asyncio
async def test_api_v1_session_mappings_get_params_x_ip(
    async_test_app: AsyncClient,
    generate_session_mapping_metrics: list[NATSessionMapping],
):
    record = choice(generate_session_mapping_metrics)

    params = {"x_ip": record.x_ip}
    response = await async_test_app.get("/v1/session_mappings/", params=params)
    data = response.json()

    for session in data:
        assert session["x_ip"] == record.x_ip


@pytest.mark.asyncio
async def test_api_v1_session_mappings_get_params_x_port(
    async_test_app: AsyncClient,
    generate_session_mapping_metrics: list[NATSessionMapping],
):
    record = choice(generate_session_mapping_metrics)

    params = {"x_port": record.x_port}
    response = await async_test_app.get("/v1/session_mappings/", params=params)
    data = response.json()

    for session in data:
        assert session["x_port"] == record.x_port


@pytest.mark.asyncio
async def test_api_v1_session_mappings_get_params_src_ip(
    async_test_app: AsyncClient,
    generate_session_mapping_metrics: list[NATSessionMapping],
):
    record = choice(generate_session_mapping_metrics)

    params = {"src_ip": record.src_ip}
    response = await async_test_app.get("/v1/session_mappings/", params=params)
    data = response.json()

    for session in data:
        assert session["src_ip"] == record.src_ip


@pytest.mark.asyncio
async def test_api_v1_session_mappings_get_params_src_port(
    async_test_app: AsyncClient,
    generate_session_mapping_metrics: list[NATSessionMapping],
):
    record = choice(generate_session_mapping_metrics)

    params = {"src_port": record.src_port}
    response = await async_test_app.get("/v1/session_mappings/", params=params)
    data = response.json()

    for session in data:
        assert session["src_port"] == record.src_port


@pytest.mark.asyncio
async def test_api_v1_session_mappings_get_params_dst_ip(
    async_test_app: AsyncClient,
    generate_session_mapping_metrics: list[NATSessionMapping],
):
    record = choice(generate_session_mapping_metrics)

    params = {"dst_ip": record.dst_ip}
    response = await async_test_app.get("/v1/session_mappings/", params=params)
    data = response.json()

    for session in data:
        assert session["dst_ip"] == record.dst_ip


@pytest.mark.asyncio
async def test_api_v1_session_mappings_get_params_dst_port(
    async_test_app: AsyncClient,
    generate_session_mapping_metrics: list[NATSessionMapping],
):
    record = choice(generate_session_mapping_metrics)

    params = {"dst_port": record.dst_port}
    response = await async_test_app.get("/v1/session_mappings/", params=params)
    data = response.json()

    for session in data:
        assert session["dst_port"] == record.dst_port
