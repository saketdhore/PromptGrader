import asyncio
import pytest
import pytest_asyncio
import logging
from httpx import AsyncClient, ASGITransport
from app.main import app
import os

os.environ["ENV"] = "test"

# ✅ This ensures the right event loop for asyncio mode
@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()

# ✅ Async test client
@pytest_asyncio.fixture(scope="function")
async def async_client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client

# ✅ Silences logs during test runs
@pytest.fixture(autouse=True)
def disable_logging():
    logging.disable(logging.CRITICAL)
    yield
    logging.disable(logging.NOTSET)
