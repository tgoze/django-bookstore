from django.shortcuts import render, redirect, reverse
from django.http import JsonResponse
from django.views.generic import TemplateView

from decimal import Decimal

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
from Store.Model.inventory_dao import InventoryDao
from Store.Model.book_order import BookOrder
from Store.Model.book_order_dao import BookOrderDao

from django.views.decorators.cache import never_cache

from Store.forms import ShipPayForm, CartForm

def update_cart_view(request):
    # Set up the cart form to receive data 
    cart_dao = CartDao() 
    user_id = request.session['user_id']
    cart_items = cart_dao.get_all(user_id)
    # An array of arrays of choices for each book
    qtys_choices = []
    # An array of book IDs to pass to the cart form
    book_ids = []
    for item in cart_items:
        # Get quantities on hand of each item in cart
        qty_on_hand = item.book.inventory.quantity_on_hand
        qty_choices = []
        for i in range(1, (qty_on_hand+1)):
            qty_choices.append((i, i))
        qtys_choices.append(qty_choices)    

        # Append book ID to list
        book_ids.append(item.book.book_id)
    
    cart_form = CartForm(request.POST, book_ids=book_ids, qtys_choices=qtys_choices)

    # Process data and update any cart items
    if cart_form.is_valid():
        response_data = {}  
        try:      
            for i, qty in enumerate(cart_form.item_fields()):
                cart = Cart()
                cart.book.book_id = cart_form.book_ids[i]
                cart.user_id = user_id
                cart.quantity_ordered = qty
                # Check whether or not the particluar item was changed and update if so                 
                if qty != str(cart_items[i].quantity_ordered):
                    updated_cart = cart_dao.update(cart)
            
            # Update prices of items
            cart_total = 0
            item_prices = []
            for item in updated_cart:            
                cart_total += item.total_item_price
                item_prices.append(item.total_item_price)

            response_data['cart_total'] = str(cart_total)
            if cart_total >= 75:
                response_data['discount_price'] = round((cart_total * Decimal(0.9)), 2)
            response_data['item_prices'] = item_prices
        except:
            response_data['message'] = "There was an error communicating with the database!" 

        return JsonResponse(response_data)
    else:
        return redirect(reverse('cart'))


class CartView(TemplateView):
    template_name = 'Store/customer/cart.html'
    inventory_dao = InventoryDao()
    cart_dao = CartDao() 

    @never_cache
    def get(self, request):
        context = {}
        if 'user_id' in request.session:
            user_id = request.session['user_id']
            cart_items = self.cart_dao.get_all(user_id)
            username = request.session['username'] 
            cart_total = 0
            # An array of arrays of choices for each book
            qtys_choices = []
            # An array of book IDs to pass to the cart form
            book_ids = []
            # A dictionary for all of the initial choices
            initial_data = {}
            for index, item in enumerate(cart_items):
                cart_total += (item.book.inventory.retail_price * item.quantity_ordered)

                # Get quantities on hand of each item in cart
                qty_on_hand = self.inventory_dao.get_byid(item.book.book_id).quantity_on_hand
                qty_choices = []
                for i in range(1, (qty_on_hand+1)):
                    qty_choices.append((i, i))
                qtys_choices.append(qty_choices)

                # Append initial data for each item to the dictionary
                initial_data['qty_choice_%s' % index] = item.quantity_ordered

                # Append book ID to list
                book_ids.append(item.book.book_id)
            
            cart_form = CartForm(initial_data, book_ids=book_ids, qtys_choices=qtys_choices)

            context['cart_form'] = cart_form
            context['cart_items'] = cart_items
            context['cart_total'] = cart_total
            if cart_total >= 75:
                context['discount_price'] = round((cart_total * Decimal(0.9)), 2)
            context['user_id'] = user_id
            context['username'] = username
        else:
            return redirect(reverse('login'))

        return render(request, self.template_name, context)

    def post(self, request):        
        user_id = request.session['user_id']

        if 'delete-item' in request.POST:
            cart_dao = CartDao()
            book_id = int(request.POST.get('delete-item'))
            cart_dao.delete_from_cart(book_id, user_id)            

        return redirect(reverse('cart'))


class ShipPayView(TemplateView):
    template_name = 'Store/customer/shippay.html'
    payment_dao = PaymentInfoDao()
    customer_address_dao = CustomerAddressDao()

    @never_cache
    def get(self, request):
        context = {}
        if 'user_id' in request.session:
            user_id = request.session['user_id']
            username = request.session['username'] 
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

            if not card_choices:
                context['notification'] = "Fill out your card information!"
            elif not shipping_choices:
                context['notification'] = "Fill out your shipping information!"
            else: 
                shippay_form = ShipPayForm(card_choices=card_choices, shipping_choices=shipping_choices)
                context['shippay_form'] = shippay_form
            
            context['cards'] = cards            
            context['user_id'] = user_id
            context['username'] = username
        else:
            return redirect(reverse('login'))

        return render(request, self.template_name, context)

    def post(self, request):
        # Gets form data
        context = {}
        user_id = request.session['user_id']
        username = request.session['username'] 
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
                context['username'] = request.session['username']
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
                username = request.session['username'] 

                cart_total = 0
                for item in cart_items:
                    cart_total += (item.total_item_price)
                
                context = {
                    'payment_choice': payment_choice,
                    'shipping_choice': shipping_choice,
                    'cart_items': cart_items,
                    'cart_total': cart_total,
                    'user_id': request.session['user_id'],
                    'username': username
                }
               
                if cart_total >= 75:
                    context['discount_price'] = round((cart_total * Decimal(0.9)), 2)
                    request.session['discount'] = 0.1
                else:
                    request.session['discount'] = 0.0

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
                retail_order.discount = request.session['discount']

                # Submit order information to server
                order_id = self.retail_order_dao.create(retail_order)

                context['notification'] = "Order made!"
            except:
                print("Error occured")
                context['notification'] = "Error!"
        
        return redirect(reverse('invoice', kwargs={ 'order_id': order_id }))


class InvoiceView(TemplateView):
    template_name = 'Store/customer/invoice.html'
    retail_order_dao = RetailOrderDao() 
    book_order_dao = BookOrderDao()
    payment_dao = PaymentInfoDao()

    @never_cache
    def get(self, request, order_id):
        if 'user_id' in request.session:
            if 'payment_choice' in request.session:
                # Get data from db to show order summary
                user_id = request.session['user_id']                
                order = self.retail_order_dao.get_byid(order_id)                
                books = self.book_order_dao.get_byid(order_id)                
                payment_info = self.payment_dao.get_byid(order.card.card_id)

                context = {
                    'order': order,
                    'books': books,
                    'user_id': user_id,
                    'username': request.session['username'],
                    'payment_info': payment_info
                }
                if order.discount > 0:
                    context['discount_price'] = round((order.total_price * Decimal((1 - order.discount))), 2)
            else:
                return redirect(reverse('ship_pay'))
        else: 
            return redirect(reverse('login'))

        return render(request, self.template_name, context)