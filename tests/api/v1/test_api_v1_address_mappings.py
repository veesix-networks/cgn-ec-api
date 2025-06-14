from secrets import choice

import pytest
from httpx import AsyncClient

from cgn_ec_api.models.metrics import (
    NATAddressMapping,
)


@pytest.mark.asyncio
async def test_api_v1_address_mappings_get(async_test_app):
    response = await async_test_app.get("/v1/address_mappings/")
    data = response.json()

    assert len(data) >= 1


@pytest.mark.asyncio
async def test_api_v1_address_mappings_get_params_limit(async_test_app: AsyncClient):
    params = {"limit": 10}
    response = await async_test_app.get("/v1/address_mappings/", params=params)
    data = response.json()
    assert len(data) == 10


@pytest.mark.asyncio
async def test_api_v1_address_mappings_get_params_skip(async_test_app: AsyncClient):
    params = {"limit": 10}
    response1 = await async_test_app.get("/v1/address_mappings/", params=params)
    data1 = response1.json()

    params["skip"] = 10
    response2 = await async_test_app.get("/v1/address_mappings/", params=params)
    data2 = response2.json()

    assert data1 != data2


@pytest.mark.asyncio
async def test_api_v1_address_mappings_get_params_x_ip(
    async_test_app: AsyncClient,
    generate_address_mapping_metrics: list[NATAddressMapping],
):
    record = choice(generate_address_mapping_metrics)

    params = {"x_ip": record.x_ip}
    response = await async_test_app.get("/v1/address_mappings/", params=params)
    data = response.json()

    for session in data:
        assert session["x_ip"] == record.x_ip


@pytest.mark.asyncio
async def test_api_v1_address_mappings_get_params_src_ip(
    async_test_app: AsyncClient,
    generate_address_mapping_metrics: list[NATAddressMapping],
):
    record = choice(generate_address_mapping_metrics)

    params = {"src_ip": record.src_ip}
    response = await async_test_app.get("/v1/address_mappings/", params=params)
    data = response.json()

    for session in data:
        assert session["src_ip"] == record.src_ip
