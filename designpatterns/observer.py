#designpatterns/observer.py
from abc import ABC, abstractmethod
from notifications.models import Notification

#subject interface
class BookingNotifier(ABC):
    @abstractmethod
    def __init__(self):
        self._observers = []

    @abstractmethod
    def register(self, observer):
        self._observers.append(observer)

    @abstractmethod
    def remove(self, observer):
        self._observers.remove(observer)

    @abstractmethod
    def notify(self, booking):
        for observer in self._observers:
            observer.update(booking)

#observer interface
class Observer(ABC):
    @abstractmethod
    def update(self, booking):
        pass

#concrete observer
class InAppNotification(Observer):
    def update(self, booking):
        message = f"Your booking for {booking.car.model} is now {booking.status}."
        Notification.objects.create(user=booking.owner, message=message)
        Notification.objects.create(user=booking.renter, message=message)


