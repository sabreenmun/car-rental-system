#This is where the builder pattern functionality goes.
from datetime import timedelta
from cars.models import Car
from abc import ABC, abstractmethod

# abstract builder
class CarBuilder(ABC):
    @abstractmethod
    def set_owner(self, owner):
        pass

    @abstractmethod
    def set_model(self, model):
        pass

    @abstractmethod
    def set_image(self, image):
        pass

    @abstractmethod
    def set_year(self, year):
        pass

    @abstractmethod
    def set_mileage(self, mileage):
        pass

    @abstractmethod
    def set_pickup_location(self, pickup_location):
        pass

    @abstractmethod
    def set_rental_price(self, rental_price):
        pass

    @abstractmethod
    def set_available_dates(self, available_from, available_to):
        pass

    @abstractmethod
    def build(self):
        pass

# Concrete builder class
class ConcreteCarBuilder(CarBuilder):
    def __init__(self):
        self.car = Car()  # create a new car object to build
    
    def set_owner(self, owner):
        self.car.owner = owner
        return self

    def set_model(self, model):
        self.car.model = model
        return self

    def set_image(self, image):
        self.car.image = image
        return self

    def set_year(self, year):
        self.car.year = year
        return self

    def set_mileage(self, mileage):
        self.car.mileage = mileage
        return self

    def set_pickup_location(self, pickup_location):
        self.car.pickup_location = pickup_location
        return self

    def set_rental_price(self, rental_price):
        self.car.rental_price = rental_price
        return self

    def set_available_dates(self, available_from, available_to):
        self.car.available_from = available_from
        self.car.available_to = available_to
        return self

    def build(self):
        return self.car


 # Director class (Car Director)
class CarDirector:
    def __init__(self, builder: CarBuilder):
        self.builder = builder

    def construct_car(self, owner, model, image, year, mileage, pickup_location, rental_price, available_from, available_to):
        return (self.builder
                .set_owner(owner)
                .set_model(model)
                .set_image(image)
                .set_year(year)
                .set_mileage(mileage)
                .set_pickup_location(pickup_location)
                .set_rental_price(rental_price)
                .set_available_dates(available_from, available_to)
                .build())  #build the car
