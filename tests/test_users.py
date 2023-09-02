import pytest
from app import schemas
from app.config import settings
from jose import jwt
from .database import client, session

@pytest.fixture
def test_user(client):
    req_body = {
        'email': 'user@example.com',
        'password': 'string'
    }
    res = client.post('/users/', json=req_body)
    user = res.json()
    user['password'] = req_body['password']
    return user

def test_root(client):
    res = client.get('/')
    excepted = 'Welcome to my API'
    assert 200 == res.status_code
    assert excepted == res.json().get('message')

def test_create_user(client):
    expected_email = 'user@example.com'
    expected_password = 'string'

    # get response as JSON
    res = client.post('/users/', json={
        'email': expected_email,
        'password': expected_password
    })
    # desserialize JSON into schemas.UserResponse object
    res_user = schemas.UserResponse(**res.json())

    assert 201 == res.status_code
    assert expected_email == res_user.email

def test_login_user(client, test_user):
    res = client.post('/login', data={
        'username': test_user['email'],
        'password': test_user['password']
    })
    res_token = schemas.Token(**res.json())

    payload = jwt.decode(res_token.access_token, settings.secret_key, algorithms=[settings.algorithm])
    id = payload.get('user_id')
    assert 200 == res.status_code
    assert test_user['id'] == id
    assert res_token.token_type == 'bearer'