from fastapi.testclient import TestClient
from app.main import app
from app.models.user import UserPublic
from unittest.mock import patch

client = TestClient(app)

def test_update_user_unauthorized(db_session):
    with patch("app.controllers.auth_controller.get_current_user") as mock_user:
        mock_user.return_value = UserPublic(
            user_id=2,
            role="user",
            email="other@example.com",
            name="Other"
        )
        response = client.put(
            "/user/1?name=Updated%20User&email=updated%40example.com",
            headers={"Authorization": "Bearer dummy_token"}
        )
        assert response.status_code == 422