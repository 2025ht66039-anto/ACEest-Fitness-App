import pytest
import os
from app import app

@pytest.fixture
def client():
    # Fix: Tell Flask where the templates folder is located
    app.config['TEMPLATE_FOLDER'] = os.path.join(os.path.dirname(__file__), '..', 'templates')
    app.testing = True
    with app.test_client() as c:
        yield c

def test_homepage(client):
    r = client.get("/")
    assert r.status_code == 200