import pytest
from app import schemas
from .database import client, session

@pytest.fixture
def test_user(client):
    req_body = {
        'email': 'user@example.com',
        'password': 'string'
    }
    res = client.post("/users/", json=req_body)
    user = res.json()
    user['password'] = req_body['password']
    return user

def test_root(client):
    res = client.get("/")
    excepted = 'Welcome to my API'
    assert 200 == res.status_code
    assert excepted == res.json().get('message')

def test_create_user(client):
    expected_email = 'user@example.com'
    expected_password = 'string'
    res = client.post("/users/", json={
        "email": expected_email,
        "password": expected_password
    })
    res_user = schemas.UserResponse(**res.json())
    assert 201 == res.status_code
    assert expected_email == res_user.email

def test_login_user(client, test_user):
    res = client.post("/login", data={
        "username": test_user['email'],
        "password": test_user['password']
    })
    assert 200 == res.status_code
    assert res.json().get('access_token')
    assert res.json().get('token_type')