# designpatterns/observer.py
from abc import ABC, abstractmethod
from notifications.models import Notification

#SUBJECT INTERFACE
class Subject(ABC):
    @abstractmethod
    def register_observer(self, observer):
        pass

    @abstractmethod
    def remove_observer(self, observer):
        pass

    @abstractmethod
    def notify_observers(self, message):
        pass

# OBSERVER INTERFACE (Abstract Class)
class Observer(ABC):
    @abstractmethod
    def update(self, message):
        pass

# CONCRETE OBSERVER
class ConcreteObserver(Observer):
    def __init__(self, user):
        self.user = user

    def update(self, message):
        Notification.objects.create(user=self.user, message=message)
        print(f"Notification sent to {self.user.username}: {message}")

# CONCRETE SUBJECT
class NotificationSystem(Subject):
    def __init__(self):
        self._observers = []

    def register_observer(self, observer):
        if observer not in self._observers:
            self._observers.append(observer)

    def remove_observer(self, observer):
        if observer in self._observers:
            self._observers.remove(observer)

    def notify_observers(self, message):
        for observer in self._observers:
            observer.update(message)

#notify users in views