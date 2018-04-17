from django.shortcuts import render
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
from Store.Model.customer_address import CustomerAddress
from django.conf import settings
from django.contrib.auth.hashers import check_password, BCryptPasswordHasher,make_password

from Store.forms import *
from bcrypt import *

class TestView(TemplateView):
    user = User()
    template_name = 'Store/customer/test.html'
    def get(self,request):
        fav_color = request.session['fav_color']
        context = {
            'fav_color':fav_color
        }

        return render(request,self.template_name,context)


class AdminCustomerView(TemplateView):
    template_name = 'Store/admin/customers/customers.html'
    
    def get(self,request):
        cdao = CustomerInfoDAO()

        customers = cdao.get_all()
        context = {
            'customers': customers
        }
        return render(request, self.template_name, context)


class AdminCustomerDetailView(TemplateView):
    template_name = 'Store/admin/customers/details.html'
    cdao = CustomerInfoDAO()
    
    def get(self, request, customer_id):
        customer = self.cdao.get_byid(customer_id)
        customer_address = self.cdao.get_addressbyid(customer_id)
        context = {
            'customer': customer,
            'caddress': customer_address
        }

        return render(request, self.template_name, context)
