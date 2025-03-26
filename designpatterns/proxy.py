import random

class PaymentGateway:
    """
    Real Payment Processor (in a real-world scenario, this would interact with Stripe, PayPal, etc.)
    """
    def process_payment(self, amount, user):
        raise NotImplementedError("Subclasses must implement process_payment()")


class PaymentGatewayProxy(PaymentGateway):
    """
    Proxy Class - Fake Payment Processor
    """
    def process_payment(self, amount, user):
        """
        Simulate a fake payment processing.
        """
        success = True  # Always succeeds (for now)
        transaction_id = f"TXN{random.randint(10000, 99999)}"

        return {
            "status": "completed" if success else "failed",
            "transaction_id": transaction_id
        }
