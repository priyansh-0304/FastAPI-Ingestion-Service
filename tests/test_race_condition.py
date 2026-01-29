import asyncio
import pytest
from httpx import AsyncClient, ASGITransport

from app.main import app


@pytest.mark.asyncio
async def test_race_condition():
    transport = ASGITransport(app=app)

    async with AsyncClient(
        transport=transport,
        base_url="http://test"
    ) as client:

        payload1 = {"sequence": 1, "data": "a", "timestamp": 1.0}
        payload2 = {"sequence": 2, "data": "b", "timestamp": 2.0}

        await asyncio.gather(
            client.post("/v1/call/stream/test-call", json=payload1),
            client.post("/v1/call/stream/test-call", json=payload2),
        )

        response = await client.post(
            "/v1/call/stream/test-call",
            json={"sequence": 3, "data": "c", "timestamp": 3.0}
        )

        assert response.status_code == 202