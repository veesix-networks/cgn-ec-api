import pytest


@pytest.mark.asyncio
async def test_api_v1_port_mappings_get(async_test_app):
    response = await async_test_app.get("/v1/port_mappings/")
    data = response.json()

    assert len(data) >= 1
