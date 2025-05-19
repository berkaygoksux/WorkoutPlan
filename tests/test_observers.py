from unittest.mock import patch
from app.patterns.observers import EventManager, TrainerNotifier

def test_event_manager_notify():
    event_manager = EventManager()
    notifier = TrainerNotifier()
    event_manager.subscribe(notifier)
    with patch("builtins.print") as mock_print:
        event_manager.notify("user_created", {"email": "test@example.com"})
        mock_print.assert_called_with("New user created: test@example.com")