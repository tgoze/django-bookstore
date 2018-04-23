class PaymentInfo:
    def __init__(self):
        self.card_id = None
        self.card_number = None
        self.last_four = None
        self.cvc = None
        self.expir_date = None
        self.card_issuer = None
        self.customer_id = None
        self.billing_address_id = None
        self.billing_address = None
    def get_billing_address(self):
        return self.billing_address

    def set_billing_address(self,billing_address):
        self.billing_address=billing_address