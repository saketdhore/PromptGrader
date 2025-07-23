import asyncio
import pytest
import pytest_asyncio
import logging
from httpx import AsyncClient, ASGITransport
from app.main import app
import os

# ✅ Set test mode early
os.environ["ENV"] = "test"

# ✅ Force an event loop for all tests
@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()

# ✅ Async test client fixture
@pytest_asyncio.fixture(scope="module")
async def async_client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client

# ✅ Mute logs during tests
@pytest_asyncio.fixture(autouse=True)
def disable_logging():
    logging.disable(logging.CRITICAL)
    yield
    logging.disable(logging.NOTSET)
