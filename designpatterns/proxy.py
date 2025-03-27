import random

class PaymentService:
    def process_payment(self, amount):
        """
        Simulate actual payment processing logic.
        """
        print(f'Processing payment of ${amount}')
        # Simulate payment success or failure
        return True  # Assume it's always successful for this example


class PaymentProxy:
    def __init__(self, payment_service):
        """
        The Proxy class that delegates the actual payment processing to PaymentService.
        """
        self.payment_service = payment_service

    def make_payment(self, amount):
        """
        Add any extra logic here (logging, validation, etc.) before delegating to PaymentService.
        """
        print(f'Processing payment through proxy: ${amount}')
        return self.payment_service.process_payment(amount)


class PaymentGatewayProxy:
    def __init__(self):
        """
        The Gateway Proxy that uses PaymentProxy to handle payments.
        """
        self.payment_service = PaymentService()  # The real payment service
        self.payment_proxy = PaymentProxy(self.payment_service)  # The proxy for payment service

    def process_payment(self, amount, user):
        """
        The method that the view will call to process the payment.
        """
        success = self.payment_proxy.make_payment(amount)

        # Simulate generating a unique transaction ID
        transaction_id = f"TXN{random.randint(10000, 99999)}"
        
        if success:
            return {"status": "completed", "transaction_id": transaction_id}
        else:
            return {"status": "failed", "transaction_id": transaction_id}
