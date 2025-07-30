import sys
import asyncio
import os
import logging
import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from asgi_lifespan import LifespanManager
from app.main import app

# Fix event loop mismatch on Windows + asyncpg
if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# Disable logging in tests
@pytest.fixture(autouse=True)
def disable_logging():
    logging.disable(logging.CRITICAL)
    yield
    logging.disable(logging.NOTSET)

# Tell app we're running tests
os.environ["ENV"] = "test"

@pytest_asyncio.fixture
async def async_client():
    async with LifespanManager(app):
        app.state.system_instructions = {
            "grader": {
                "master": "Fake instructions for testing"
            },
            "consultant": {
                "master": "Fake instructions for testing"
            },
            "engineer": {
                "master": "Fake instructions for testing"
            }
        }
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            yield client
