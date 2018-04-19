from django.shortcuts import render
from django.views.generic import TemplateView

from Store.Model.cart_dao import CartDao
from Store.Model.cart import Cart

class CartView(TemplateView):
    template_name = 'Store/customer/cart.html'
    cart_dao = CartDao() 

    def get(self, request):
        loggedin_user_id = request.session['user_id']
        cart_items = self.cart_dao.get_all(loggedin_user_id)
        context = {
            'cart_items': cart_items,
            'loggedin_user_id': loggedin_user_id
        }
        return render(request, self.template_name, context)

    def post(self, request):
        context = {}
        return render(request, self.template_name, context)