from django.shortcuts import render, redirect, reverse
from django.views.generic import TemplateView
from Store.Model.book import Book
from Store.Model.book_dao import BookDao
from Store.Model.author import Author
from Store.Model.author_dao import AuthorDao
from Store.Model.publisher import Publisher
from Store.Model.publisher_dao import PublisherDao
from Store.Model.genre import Genre
from Store.Model.genre_dao import GenreDao
from Store.Model.customer_info_dao import CustomerInfoDAO
from Store.Model.user import User
from Store.Model.user_dao import UserDao
from Store.Model.customer_info import CustomerInfo
from Store.Model.customer_address_dao import CustomerAddressDao
from Store.Model.customer_address import CustomerAddress
from Store.Model.payment_info import PaymentInfo
from Store.Model.payment_info_dao import PaymentInfoDao
from Store.Model.inventory import Inventory
from Store.Model.inventory_dao import InventoryDao
from Store.Model.retail_order import RetailOrder
from Store.Model.retail_order_dao import RetailOrderDao
from Store.Model.book_order import BookOrder
from Store.Model.book_order_dao import BookOrderDao
from django.conf import settings
from django.contrib.auth.hashers import check_password, BCryptPasswordHasher,make_password
from Store.forms import *
from bcrypt import *
from django.views.decorators.cache import never_cache

class AdminOrderView(TemplateView):
    template_name = 'Store/admin/orders/orders.html'
    odao = RetailOrderDao()

    @never_cache
    def get(self,request):
        orders = self.odao.get_all()
        context = {
            'orders': orders
        }
        user_id =  request.session['user_id'] 
        username = request.session['username'] 
        context['user_id'] = request.session['user_id']
        context['username'] = request.session['username']
        return render(request,self.template_name, context) 
    
    @never_cache
    def post(self,request):
        context={}
        user_id =  request.session['user_id'] 
        username = request.session['username'] 
        context['user_id'] = request.session['user_id']
        context['username'] = request.session['username']
        return render(request,self.template_name, context) 
    
class AdminOrderDetailView(TemplateView): 
    template_name = 'Store/admin/orders/details.html'
    odao = RetailOrderDao()
    pdao = PaymentInfoDao()
    bodao = BookOrderDao()
    bdao = Book()
    @never_cache
    def get(self, request, order_id):
        order = self.odao.get_byid(order_id)
        bookorder = self.bodao.get_byid(order_id)
       
        context = {
            'order': order,
            'bookorder':bookorder
        }
        user_id =  request.session['user_id'] 
        username = request.session['username'] 
        context['user_id'] = request.session['user_id']
        context['username'] = request.session['username']
        return render(request, self.template_name, context)
