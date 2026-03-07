from app import web_app

def test_home():
    client = web_app.test_client()
    response = client.get("/")
    assert response.status_code == 200