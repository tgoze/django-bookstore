class CustomerInfo:
    def __init__(self):
        self.customer_id = None
        self.work_phone = None
        self.home_phone = None
        self.user = None 
        self.address = None
        self.payment_info = None
    def get_user(self):
        return self.user

    def set_user(self,user):
        self.user=user
    
    def get_address(self):
        return self.address

    def set_address(self,address):
        self.address=address
    
    def get_payment_info(self):
        return self.payment_info

    def set_payment_info(self,payment_info):
        self.payment_info=payment_info