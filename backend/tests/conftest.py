import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from unittest.mock import patch
from app.core.database import get_db
from app.models.models import Base

TEST_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture(scope="session", autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)
    engine.dispose()
    if os.path.exists("test.db"):
        try:
            os.remove("test.db")
        except PermissionError:
            pass

@pytest.fixture
def client(setup_database):
    # Patch init_db before app starts so it never touches PostgreSQL
    with patch("app.core.database.init_db", return_value=None):
        from app.main import app
        app.dependency_overrides[get_db] = override_get_db
        with TestClient(app) as c:
            yield c
        app.dependency_overrides.clear()

@pytest.fixture
def db(setup_database):
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()