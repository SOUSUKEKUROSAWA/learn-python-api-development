import pytest
from app import schemas
from app.config import settings
from app.database import get_db, Base
from app.main import app
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.db_user}:{settings.db_password}_test@{settings.db_host}_test/{settings.db_name}_test"
SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.db_user}:{settings.db_password}@{settings.db_host}/{settings.db_name}_test"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture
def client():
    Base.metadata.create_all(bind=engine)
    yield TestClient(app) # yieldの時点でテストが実行される=>テスト前後の処理を記述できるようになる
    Base.metadata.drop_all(bind=engine)

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