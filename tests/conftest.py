import pytest
from fastapi.testclient import TestClient
from app.main import app
from unittest.mock import Mock
from app.database import SessionLocal

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def db_session():
    return Mock(spec=SessionLocal)