from django.shortcuts import render, redirect, reverse
from django.views.generic import TemplateView

from Store.Model.cart_dao import CartDao
from Store.Model.cart import Cart
from Store.Model.payment_info import PaymentInfo
from Store.Model.payment_info_dao import PaymentInfoDao
from Store.Model.customer_address import CustomerAddress
from Store.Model.customer_address_dao import CustomerAddressDao
from Store.Model.retail_order import RetailOrder
from Store.Model.retail_order_dao import RetailOrderDao
from Store.Model.customer_info import CustomerInfo
from Store.Model.customer_info_dao import CustomerInfoDAO

from django.views.decorators.cache import never_cache

from Store.forms import ShipPayForm


class CartView(TemplateView):
    template_name = 'Store/customer/cart.html'
    cart_dao = CartDao() 

    @never_cache
    def get(self, request):
        context = {}
        if 'user_id' in request.session:
            user_id = request.session['user_id']
            cart_items = self.cart_dao.get_all(user_id)
            
            cart_total = 0
            for item in cart_items:
                cart_total += (item.book.inventory.retail_price * item.quantity_ordered)

            context['cart_items'] = cart_items
            context['cart_total'] = cart_total
            context['user_id'] = user_id

        else:
            return redirect(reverse('login'))

        return render(request, self.template_name, context)

    def post(self, request):
        context = {}
        user_id = request.session['user_id']

        if 'delete-book' in request.POST:
            book_id = int(request.POST.get('delete-book'))
            self.cart_dao.delete_from_cart(book_id, user_id)

        cart_items = self.cart_dao.get_all(user_id)
            
        cart_total = 0
        for item in cart_items:
            cart_total += (item.book.inventory.retail_price * item.quantity_ordered)

        context['cart_items'] = cart_items
        context['cart_total'] = cart_total
        context['user_id'] = user_id

        return render(request, self.template_name, context)


class ShipPayView(TemplateView):
    template_name = 'Store/customer/shippay.html'
    payment_dao = PaymentInfoDao()
    customer_address_dao = CustomerAddressDao()

    @never_cache
    def get(self, request):
        context = {}
        if 'user_id' in request.session:
            user_id = request.session['user_id']
            cards =  self.payment_dao.get_by_customer_id(user_id)
            ship_addresses = self.customer_address_dao.get_by_customer_and_type(user_id, "Shipping")

            # This code organizes the credit card info and shipping info so that the Django form can handle it
            # The choice field in the forms class takes a list of tuples for choices
            card_choices = []
            for card in cards:
                card_val = (str(card.card_id), str(card.card_issuer) + " card ending in " + str(card.last_four))
                card_choices.append(card_val)
            shipping_choices = []
            for address in ship_addresses:
                address_val = (str(address.address_id), str(address.street) + " " + str(address.city) + ", " 
                    + str(address.state_code) + " " + str(address.zip_code))
                shipping_choices.append(address_val)

            shippay_form = ShipPayForm(card_choices=card_choices, shipping_choices=shipping_choices)
            context['shippay_form'] = shippay_form
            context['cards'] = cards            
            context['user_id'] = user_id
        else:
            return redirect(reverse('login'))

        return render(request, self.template_name, context)

    def post(self, request):
        # Gets form data
        user_id = request.session['user_id']
        cards = self.payment_dao.get_by_customer_id(user_id)
        ship_addresses = self.customer_address_dao.get_by_customer_and_type(user_id, "Shipping")

        # This code organizes the credit card info and shipping info so that the Django form can handle it
        # The choice field in the forms class takes a list of tuples for choices
        card_choices = []
        for card in cards:
            card_val = (str(card.card_id), str(card.card_issuer) + " card ending in " + str(card.last_four))
            card_choices.append(card_val)
        shipping_choices = []
        for address in ship_addresses:
            address_val = (str(address.address_id), str(address.street) + " " + str(address.city) + ", " 
                + str(address.state_code) + " " + str(address.zip_code))
            shipping_choices.append(address_val)

        shippay_form = ShipPayForm(request.POST, card_choices=card_choices, shipping_choices=shipping_choices)

        # Validate POST data
        if 'review-order' in request.POST:
            if shippay_form.is_valid():
                # Get choice of payment and shipping address
                payment_choice_id = shippay_form.cleaned_data['credit_cards']
                shipping_choice_id = shippay_form.cleaned_data['shipping_addresses']             

                request.session['payment_choice'] = payment_choice_id
                request.session['shipping_choice'] = shipping_choice_id                
                        
        return redirect(reverse('checkout'))


class CheckOutView(TemplateView):
    template_name = 'Store/customer/checkout.html'
    retail_order_dao = RetailOrderDao() 
    payment_dao = PaymentInfoDao()
    customer_address_dao = CustomerAddressDao()
    cart_dao = CartDao()

    @never_cache
    def get(self, request):
        if 'user_id' in request.session:
            if 'payment_choice' in request.session:
                # Get data from db to show order summary
                payment_choice = self.payment_dao.get_byid(request.session['payment_choice'])
                shipping_choice = self.customer_address_dao.get_byid(request.session['shipping_choice'])
                cart_items = self.cart_dao.get_all(request.session['user_id'])

                cart_total = 0
                for item in cart_items:
                    cart_total += (item.book.inventory.retail_price * item.quantity_ordered)

                context = {
                    'payment_choice': payment_choice,
                    'shipping_choice': shipping_choice,
                    'cart_items': cart_items,
                    'cart_total': cart_total,
                    'user_id': request.session['user_id']
                }
            else:
                return redirect(reverse('ship_pay'))
        else:
            return redirect(reverse('login'))

        return render(request, self.template_name, context)

    def post(self, request):
        retail_order = RetailOrder()
        context = {}

        if 'place-order' in request.POST:
            try:
                # Get data from form
                retail_order.customer.customer_id = request.session['user_id']
                retail_order.shipping_address.address_id = request.POST['shipping_choice']                
                retail_order.card.card_id = request.POST['payment_choice']

                # Submit order information to server
                self.retail_order_dao.create(retail_order)

                context['notification'] = "Order made!"
            except:
                print("Error occured")
                context['notification'] = "Error!"
        
        return redirect(reverse('invoice'))


class InvoiceView(TemplateView):
    template_name = 'Store/customer/invoice.html'
    retail_order_dao = RetailOrderDao() 
    payment_dao = PaymentInfoDao()
    customer_address_dao = CustomerAddressDao()
    customer_dao = CustomerInfoDAO()
    cart_dao = CartDao()

    @never_cache
    def get(self, request):
        if 'user_id' in request.session:
            if 'payment_choice' in request.session:
                # Get data from db to show order summary
                user_id = request.session['user_id']
                payment_choice = self.payment_dao.get_byid(request.session['payment_choice'])
                shipping_choice = self.customer_address_dao.get_byid(request.session['shipping_choice'])
                cart_items = self.cart_dao.get_all(user_id)
                customer_info = self.customer_dao.get_byid(user_id)

                cart_total = 0
                for item in cart_items:
                    cart_total += (item.book.inventory.retail_price * item.quantity_ordered)

                context = {
                    'payment_choice': payment_choice,
                    'shipping_choice': shipping_choice,
                    'cart_items': cart_items,
                    'cart_total': cart_total,
                    'customer_info': customer_info,
                    'user_id': user_id
                }

            else:
                return redirect(reverse('ship_pay'))
        else: 
            return redirect(reverse('login'))

        return render(request, self.template_name, context)

    def post(self, request):
        return render(request, self.template_name)