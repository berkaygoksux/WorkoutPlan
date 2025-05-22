from app.patterns.workout_commands import CreateWorkoutPlanCommand
from app.models.workout_plan import WorkoutPlan
from unittest.mock import Mock

def test_create_workout_plan_command():
    plan_service = Mock()
    plan_data = WorkoutPlan(
        user_id=1,
        title="Test Plan",
        level="beginner",
        exercises=[{"exercise_id": 1, "sets": 3, "reps": 10}],
        start_date="2025-05-01",
        end_date="2025-05-30"
    )
    plan_service.create_plan.return_value = plan_data
    command = CreateWorkoutPlanCommand(plan_service, plan_data)
    result = command.execute(Mock())
    assert result.title == "Test Plan"