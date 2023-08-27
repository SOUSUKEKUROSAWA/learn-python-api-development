from fastapi.testclient import TestClient
from app import schemas
from app.main import app

client = TestClient(app)

def test_root():
    res = client.get("/")
    excepted = 'Welcome to my API'
    assert 200 == res.status_code
    assert excepted == res.json().get('message')

def test_create_user():
    expected_email = 'user@example.com'
    expected_password = 'string'
    res = client.post("/users/", json={
        "email": expected_email,
        "password": expected_password
    })
    res_user = schemas.UserResponse(**res.json())
    assert 201 == res.status_code
    assert expected_email == res_user.email
    assert expected_password == res_user.password