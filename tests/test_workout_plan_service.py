from app.models.workout_log import WorkoutLog
from app.services.workout_plan_service import WorkoutPlanService
from app.models.workout_plan import WorkoutPlan
from unittest.mock import Mock, patch
from datetime import date


def test_create_plan_success(db_session):
    plan_service = WorkoutPlanService()
    plan_data = WorkoutPlan(
        user_id=1,
        title="Beginner Plan",
        level="beginner",
        exercises=[{"exercise_id": 1, "sets": 3, "reps": 10, "rest_seconds": 30}],
        start_date=date(2025, 10, 1),
        end_date=date(2025, 11, 5)
    )

    mock_exercise = Mock()
    mock_exercise.exercise_id = 1
    mock_exercise.name = "Squat"
    mock_exercise.description = "Leg exercise"


    mock_query = Mock()
    mock_filter = Mock()
    mock_first = Mock(return_value=mock_exercise)
    mock_filter.first = mock_first
    mock_query.filter = Mock(return_value=mock_filter)
    db_session.query = Mock(return_value=mock_query)


    db_session.add = Mock(return_value=None)
    db_session.commit = Mock(return_value=None)
    db_session.refresh = Mock(return_value=None)

    with patch.object(plan_service, "event_manager") as mock_event_manager:
        with patch("app.services.workout_log_service.WorkoutLogService.create_log") as mock_create_log:
            mock_create_log.return_value = WorkoutLog(
                log_id=1,
                user_id=1,
                exercise_id=1,
                exercise_name="Squat",
                exercise_description="Leg exercise",
                sets=3,
                reps=10,
                date=date(2025, 10, 1),
                duration=35,
                notes="Beginner Plan"
            )
            created_plan = plan_service.create_plan(plan_data, db_session)
            assert created_plan.title == "Beginner Plan"
            mock_event_manager.notify.assert_called()