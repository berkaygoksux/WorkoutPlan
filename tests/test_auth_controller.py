from fastapi.testclient import TestClient
from app.main import app
from app.models.user import UserInDB, UserPublic

client = TestClient(app)

def test_register_user_success():

    payload = {
        "name": "Test User",
        "email": "test@example.com",
        "password": "Test123!",
        "role": "user"
    }
    response = client.post("/auth/register", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@example.com"
    assert data["name"] == "Test User"
    assert data["role"] == "user"

def test_register_user_success():
    payload = {
        "name": "Test User",
        "email": "test@example.com",
        "password": "Test123!",
        "role": "user"
    }
    with patch("app.services.user_service.UserService.get_user_by_email", return_value=None):
        with patch("app.services.user_service.UserService.create_user") as mock_create:
            mock_create.return_value = UserPublic(
                user_id=1,
                name="Test User",
                email="test@example.com",
                role="user"
            )
            response = client.post("/auth/register", json=payload)
            assert response.status_code == 200
            assert response.json()["email"] == "test@example.com"

# tests/test_auth_controller.py
from fastapi.testclient import TestClient
from app.main import app
from app.models.user import UserInDB
from unittest.mock import patch
from passlib.context import CryptContext

client = TestClient(app)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def test_login_user_success():
    payload = {
        "email": "test@example.com",
        "password": "Test123!"
    }
    # Gerçek bir bcrypt hash oluştur
    hashed_password = pwd_context.hash("Test123!")
    with patch("app.services.user_service.UserService.get_user_by_email") as mock_get_user:
        mock_get_user.return_value = UserInDB(
            user_id=1,
            email="test@example.com",
            password=hashed_password,
            role="user",
            name="Test User"
        )
        with patch("app.controllers.auth_controller.pwd_context.verify", return_value=True):
            response = client.post("/auth/login", json=payload)
            assert response.status_code == 200
            data = response.json()
            assert "access_token" in data
            assert data["token_type"] == "bearer"