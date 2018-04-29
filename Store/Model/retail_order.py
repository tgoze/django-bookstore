from Store.Model.customer_info import CustomerInfo
from Store.Model.customer_address import CustomerAddress
from Store.Model.payment_info import PaymentInfo

class RetailOrder():
    def __init__(self):
        self.order_id = None
        self.date_ordered = None
        self.total_price = None
        self.discount = None
        self.customer = CustomerInfo()
        self.shipping_address = CustomerAddress()
        self.card = PaymentInfo()
        self.status = None