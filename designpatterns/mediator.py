from abc import ABC, abstractmethod
from cars.models import Car, Booking
from cars.forms import CarSearchForm


#mediator interface
class Mediator(ABC):
    @abstractmethod
    def mediate(self, form, request):
        pass


#concrete mediator
class ConcreteMediator(Mediator):
    def __init__(self):
        self.colleague1 = None  #CarSearchLogic
        self.colleague2 = None  #CarSearchFormHandler

    def set_colleague1(self, colleague):
        self.colleague1 = colleague

    def set_colleague2(self, colleague):
        self.colleague2 = colleague

    def mediate(self, form, request):
        #mediator coordinates the behavior between colleagues
        if self.colleague2.validate(form):  #validate the form
            return self.colleague1.filter_cars(form)  #filter cars if validation is successful
        return None


#colleague 1: CarSearchLogic
class CarSearchLogic:
    def __init__(self, request):
        self.request = request

    def filter_cars(self, form):
        cars = Car.objects.all()

        # Filtering based on the form data
        model = form.cleaned_data.get('model')
        rental_price_min = form.cleaned_data.get('rental_price_min')
        rental_price_max = form.cleaned_data.get('rental_price_max')
        available_from = form.cleaned_data.get('available_from')
        available_to = form.cleaned_data.get('available_to')

        if model:
            cars = cars.filter(model__icontains=model)
        if rental_price_min:
            cars = cars.filter(rental_price__gte=rental_price_min)
        if rental_price_max:
            cars = cars.filter(rental_price__lte=rental_price_max)

        # Filter based on availability dates
        if available_from and available_to:
            cars = self.filter_by_availability(cars, available_from, available_to)

        return cars

    def filter_by_availability(self, cars, available_from, available_to):
        # Filter cars that are available in the specified date range
        available_cars = []
        
        for car in cars:
            # Get all bookings for this car
            bookings = Booking.objects.filter(car=car)

            # Check if the car is available during the specified date range
            is_available = True
            for booking in bookings:
                # Compare booking dates with the search range
                if (available_from <= booking.available_to and available_to >= booking.available_from):
                    is_available = False
                    break  # If there's a conflict, the car is not available

            if is_available:
                available_cars.append(car)

        return available_cars


#colleague 2: CarSearchFormHandler
class CarSearchFormHandler:
    def __init__(self, form):
        self.form = form

    def validate(self, form):
        if form.is_valid():
            # Validation logic for rental prices
            rental_price_min = form.cleaned_data.get('rental_price_min')
            rental_price_max = form.cleaned_data.get('rental_price_max')
            available_from = form.cleaned_data.get('available_from')
            available_to = form.cleaned_data.get('available_to')

            if rental_price_min and rental_price_max and rental_price_min > rental_price_max:
                form.add_error('rental_price_max', "The 'Max Rental Price' cannot be less than the 'Min Rental Price'.")
                return False

            if available_from and available_to and available_from > available_to:
                form.add_error('available_to', "The 'Available To' date cannot be earlier than the 'Available From' date.")
                return False

            return True
        return False
