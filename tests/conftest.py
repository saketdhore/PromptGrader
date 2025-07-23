import pytest
import pytest_asyncio
import logging
from httpx import AsyncClient, ASGITransport
from app.main import app
import os

# Set test environment before anything else
os.environ["ENV"] = "test"

# Ensure event loop is defined for module-scope async fixtures
@pytest.fixture(scope="session")
def event_loop():
    loop = pytest.asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

# Shared test client using ASGITransport (no actual server needed)
@pytest_asyncio.fixture(scope="module")
async def async_client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client

# Automatically disable logs during tests
@pytest_asyncio.fixture(autouse=True)
def disable_logging():
    logging.disable(logging.CRITICAL)
    yield
    logging.disable(logging.NOTSET)
