import pytest_asyncio
import logging
from httpx import AsyncClient
from httpx import ASGITransport
from app.main import app
import os
os.environ["ENV"] = "test"

@pytest_asyncio.fixture(scope="module")
async def async_client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client

@pytest_asyncio.fixture(autouse=True)
def disable_logging():
    logging.disable(logging.CRITICAL)
    yield
    logging.disable(logging.NOTSET)  # Re-enable logging after test
