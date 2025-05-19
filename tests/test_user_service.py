from app.services.user_service import UserService
from app.models.user import UserInDB, UserPublic
from unittest.mock import Mock, patch


def test_create_user_success():
    db_mock = Mock()
    user_service = UserService()
    user_data = UserInDB(
        name="Test User",
        email="test@example.com",
        password="Test123!",
        role="user"
    )
    db_mock.add.return_value = None
    db_mock.commit.return_value = None
    db_mock.refresh.return_value = None

    with patch.object(user_service, "event_manager") as mock_event_manager:
        created_user = user_service.create_user(user_data, db_mock)
        assert isinstance(created_user, UserPublic)
        assert created_user.email == "test@example.com"
        mock_event_manager.notify.assert_called_with("user_created", {"email": "test@example.com"})

def test_get_user_by_email_not_found():
    db_mock = Mock()
    db_mock.query.return_value.filter.return_value.first.return_value = None
    user_service = UserService()
    result = user_service.get_user_by_email("nonexistent@example.com", db_mock)
    assert result is None