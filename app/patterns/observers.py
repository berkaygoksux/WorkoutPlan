from abc import ABC, abstractmethod

class Observer(ABC):
    @abstractmethod
    def update(self, event: str, data: dict):
        pass

class EventManager:
    def __init__(self):
        self.observers = []

    def subscribe(self, observer: Observer):
        self.observers.append(observer)

    def notify(self, event: str, data: dict):
        for observer in self.observers:
            observer.update(event, data)

class TrainerNotifier(Observer):
    def update(self, event: str, data: dict):
        if event == "user_created":
            print(f"New user created: {data['email']}")
        elif event == "plan_created":
            print(f"New plan created: Plan ID {data['plan_id']}, User ID {data['user_id']}")
        elif event == "log_created":
            print(f"New log created: Log ID {data['log_id']}, User ID {data['user_id']}")
