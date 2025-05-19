from app.database import ExerciseDB
from app.services.exercise_service import ExerciseService
from app.models.exercise import Exercise
from unittest.mock import Mock

def test_create_exercise_success(db_session):
    exercise_service = ExerciseService()
    exercise_data = Exercise(
        name="Squat",
        description="Leg exercise",
        muscle_group="legs",
        exercise_type="strength"
    )
    db_session.add = Mock(return_value=None)
    db_session.commit = Mock(return_value=None)
    db_session.refresh = Mock(return_value=None)
    created_exercise = exercise_service.create_exercise(exercise_data, db_session)
    assert created_exercise.name == "Squat"

def test_get_exercise_by_id_not_found(db_session):
    exercise_service = ExerciseService()
    db_session.query = Mock(return_value=Mock(filter=Mock(return_value=Mock(first=Mock(return_value=None)))))
    exercise = exercise_service.get_exercise_by_id(1, db_session)
    assert exercise is None


def test_update_exercise_success(db_session):
    exercise_service = ExerciseService()
    exercise_data = Exercise(
        exercise_id=1,
        name="Updated Squat",
        description="Updated leg exercise",
        muscle_group="legs",
        exercise_type="strength"
    )

    mock_query = Mock()
    mock_filter = Mock()
    mock_first = Mock(return_value=exercise_data)
    mock_filter.first = mock_first
    mock_query.filter = Mock(return_value=mock_filter)
    db_session.query = Mock(return_value=mock_query)

    db_session.commit = Mock(return_value=None)
    db_session.refresh = Mock(return_value=None)

    updated_exercise = exercise_service.update_exercise(exercise_data, db_session)
    assert updated_exercise.name == "Updated Squat"


def test_delete_exercise_success(db_session):
    exercise_service = ExerciseService()
    db_exercise = ExerciseDB(
        exercise_id=1,
        name="Squat",
        description="Leg exercise",
        muscle_group="legs",
        exercise_type="strength"
    )

    mock_query = Mock()
    mock_filter = Mock()
    mock_first = Mock(return_value=db_exercise)
    mock_filter.first = mock_first
    mock_query.filter = Mock(return_value=mock_filter)
    db_session.query = Mock(return_value=mock_query)

    db_session.delete = Mock(return_value=None)
    db_session.commit = Mock(return_value=None)

    result = exercise_service.delete_exercise(1, db_session)
    assert result is True