from Store.Model.customer_address import CustomerAddress

class PaymentInfo:
    def __init__(self):
        self.card_id = None
        self.card_number = None
        self.last_four = None
        self.cvc = None
        self.expir_date = None
        self.card_issuer = None
        self.customer_id = None
        self.billing_address = CustomerAddress()