import pytest


@pytest.mark.asyncio
async def test_api_v1_session_mappings_get(async_test_app):
    response = await async_test_app.get("/v1/session_mappings/")
    data = response.json()

    assert len(data) >= 1
