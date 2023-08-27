import pytest
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

@pytest.fixture()
def session():
    db = TestingSessionLocal()
    try:
        Base.metadata.create_all(bind=engine)
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture()
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)