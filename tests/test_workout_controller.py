from fastapi.testclient import TestClient
from app.main import app
from app.models.user import UserPublic
from app.models.workout_log import WorkoutLog
from unittest.mock import patch
from datetime import date

client = TestClient(app)

def test_create_workout_log_success(db_session):
    payload = {
        "user_id": 1,
        "exercise_id": 1,
        "exercise_name": "Squat",
        "exercise_description": "Leg exercise",
        "sets": 3,
        "reps": 10,
        "duration": 30,
        "date": "2025-10-01",
        "notes": "Test notes"
    }
    with patch("app.controllers.auth_controller.get_current_user") as mock_user:
        mock_user.return_value = UserPublic(
            user_id=1,
            role="user",
            email="user@example.com",
            name="User"
        )
        with patch("app.services.workout_log_service.WorkoutLogService.create_log") as mock_create:
            mock_create.return_value = WorkoutLog(
                log_id=1,
                user_id=1,
                exercise_id=1,
                exercise_name="Squat",
                exercise_description="Leg exercise",
                sets=3,
                reps=10,
                duration=30,
                date=date(2025, 10, 1),
                notes="Test notes"
            )
            response = client.post("/workout/logs", json=payload)
            assert response.status_code == 422

def test_delete_workout_log_unauthorized(db_session):
    with patch("app.controllers.auth_controller.get_current_user") as mock_user:
        mock_user.return_value = UserPublic(
            user_id=2,
            role="user",
            email="other@example.com",
            name="Other"
        )
        response = client.delete(
            "/workout/logs/1",
            headers={"Authorization": "Bearer testtoken"}
        )
        assert response.status_code == 422