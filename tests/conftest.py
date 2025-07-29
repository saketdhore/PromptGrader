import asyncio
import pytest
import pytest_asyncio
import logging
from httpx import AsyncClient, ASGITransport
from asgi_lifespan import LifespanManager
from app.main import app
import os

os.environ["ENV"] = "test"

@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()

@pytest_asyncio.fixture(scope="function")
async def async_client():
    async with LifespanManager(app):  # 👈 ensures startup/shutdown is run
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            yield client

@pytest.fixture(autouse=True)
def disable_logging():
    logging.disable(logging.CRITICAL)
    yield
    logging.disable(logging.NOTSET)
