from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root():
    res = client.get("/")
    excepted = 'Welcome to my API'
    assert 200 == res.status_code
    assert excepted == res.json().get('message')