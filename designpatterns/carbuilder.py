from datetime import timedelta
from cars.models import Car

class CarBuilder:
    def __init__(self):
        self.car = Car()

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
        """Sets the available rental period with a start and end date."""
        self.car.available_from = available_from
        self.car.available_to = available_to
        return self

    def build(self):
        return self.car
