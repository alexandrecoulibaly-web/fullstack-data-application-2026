import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.routers import items, reservations


@pytest.fixture()
def client():
    items.FAKE_DB.clear()
    reservations.FAKE_DB.clear()
    items._next_id = 1
    reservations._next_id = 1

    with TestClient(app) as test_client:
        yield test_client

    items.FAKE_DB.clear()
    reservations.FAKE_DB.clear()
