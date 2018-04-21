from django.shortcuts import render
from django.shortcuts import redirect, reverse
from django.views.generic import TemplateView

from Store.Model.cart_dao import CartDao
from Store.Model.cart import Cart

class CartView(TemplateView):
    template_name = 'Store/customer/cart.html'
    cart_dao = CartDao() 

    def get(self, request):
        context = {}
        if 'user_id' in request.session:
            loggedin_user_id = request.session['user_id']
            cart_items = self.cart_dao.get_all(loggedin_user_id)
            
            cart_total = 0
            for item in cart_items:
                cart_total += item.book.inventory.retail_price

            context['cart_items'] = cart_items
            context['cart_total'] = cart_total
            context['loggedin_user_id'] = loggedin_user_id

        else:
            return redirect(reverse('login'))

        return render(request, self.template_name, context)

    def post(self, request):
        context = {}
        return render(request, self.template_name, context)