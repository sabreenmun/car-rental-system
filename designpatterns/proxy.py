#This is where the proxy pattern functionality goes.
from abc import ABC, abstractmethod
import random

#SUBJECT INTERFACE
class PaymentInterface(ABC):
    @abstractmethod
    def pay(self, amount, user):
        pass


#REAL SUBJECT
class RealPayment(PaymentInterface):
    def __init__(self):
        pass

    def pay(self, amount, user):
        print(f"Real payment of ${amount} for user {user} processed.")
        return True  # simulate a successful payment (only for this project)

# PROXY
class PaymentProxy(PaymentInterface):
    def __init__(self):
        self.real_payment = RealPayment()  #create an instance of the RealPayment (aka the real subject)

    def pay(self, amount, user):
        #use function from interface, override
        print(f"Proxy handling payment of ${amount} for user {user}")
        return self.real_payment.pay(amount, user)

# CLIENT
class Client:
    def __init__(self):
        self.payment_interface = PaymentProxy() #use PROXY interface, client is the gateway

    def pay_for_booking(self, amount, user):
        return self.payment_interface.pay(amount, user)