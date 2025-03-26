

class PaymentService:
    def process_payment(self, amount):
      
        print(f'Processing payment of {amount}')
        return True

class PaymentProxy:
    def __init__(self, payment_service):
        self.payment_service = payment_service

    def make_payment(self, amount):
        
        return self.payment_service.process_payment(amount)
