import pytest
from app import app

@pytest.fixture
def client():
    app.testing = True
    with app.test_client() as c:
        yield c

def test_homepage(client):
    r = client.get("/")
    assert r.status_code == 200