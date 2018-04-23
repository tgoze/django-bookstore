from django.shortcuts import render, redirect, reverse
from django.views.generic import TemplateView

from Store.Model.cart_dao import CartDao
from Store.Model.cart import Cart
from Store.Model.payment_info import PaymentInfo
from Store.Model.payment_info_dao import PaymentInfoDao
from Store.Model.customer_address import CustomerAddress
from Store.Model.customer_address_dao import CustomerAddressDao

from Store.forms import ShipPayForm


class CartView(TemplateView):
    template_name = 'Store/customer/cart.html'
    cart_dao = CartDao() 

    def get(self, request):
        context = {}
        if 'user_id' in request.session:
            user_id = request.session['user_id']
            cart_items = self.cart_dao.get_all(user_id)
            
            cart_total = 0
            for item in cart_items:
                cart_total += item.book.inventory.retail_price

            context['cart_items'] = cart_items
            context['cart_total'] = cart_total
            context['user_id'] = user_id

        else:
            return redirect(reverse('login'))

        return render(request, self.template_name, context)

    def post(self, request):
        context = {}
        return render(request, self.template_name, context)


class ShipPayView(TemplateView):
    template_name = 'Store/customer/shippay.html'
    payment_dao = PaymentInfoDao()
    customer_address_dao = CustomerAddressDao()

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
            ship_address_choices = []
            for address in ship_addresses:
                address_val = (str(address.address_id), str(address.street))
                ship_address_choices.append(address_val)

            shippay_form = ShipPayForm(card_choices, ship_address_choices)
            context['shippay_form'] = shippay_form
            context['cards'] = cards
            context['ship_addresses'] = ship_addresses
            context['user_id'] = user_id
        else:
            return redirect(reverse('login'))

        return render(request, self.template_name, context)

    def post(self, request):
        context = {}
        return render(request, self.template_name, context)


class CheckOutView(TemplateView):
    template_name = 'Store/customer/checkout.html'
    cart_dao = CartDao() 

    def get(self, request):
        context = {}
        if 'user_id' in request.session:
            user_id = request.session['user_id']
            cart_items = self.cart_dao.get_all(user_id)
            
            cart_total = 0
            for item in cart_items:
                cart_total += item.book.inventory.retail_price

            context['cart_items'] = cart_items
            context['cart_total'] = cart_total
            context['user_id'] = user_id

        else:
            return redirect(reverse('login'))

        return render(request, self.template_name, context)

    def post(self, request):
        context = {}
        return render(request, self.template_name, context)