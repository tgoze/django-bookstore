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
from Store.Model.customer_info import CustomerInfo
from Store.Model.customer_address_dao import CustomerAddressDao
from Store.Model.customer_address import CustomerAddress
from django.conf import settings
from django.contrib.auth.hashers import check_password, BCryptPasswordHasher,make_password
from Store.forms import *
from bcrypt import *


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

class CustomerIndexView(TemplateView):
    template_name = 'Store/customer/index.html'
    cus_account = 'Store/customer/customeraccount.hmtl'
    user = User()
    udao = UserDao()
    def get(self,request):
        return render(request, self.template_name,context=None)
    def post(self,request, user_id):
        context = {}
        user = self.udao.get_byid(user_id)
        request.session['user_id'] = user.id
        request.session['username'] = user.username
        context['user_id'] = request.session['user_id'],
        context['username'] = request.session['username'] 
        return render(request, self.cus_account,context)     
class CustomerAccountView(TemplateView):
    template_name = 'Store/customer/customeraccount.html'
    user = User()
    udao = UserDao()
    customer = CustomerInfo()
    cdao = CustomerInfoDAO()
    cusadd = CustomerAddress()
    cadao = CustomerAddressDao()
    def get(self,request,user_id):
        customer = self.cdao.get_byid(user_id)
        caddress = self.cadao.get_all_addresses_by_customer_id(user_id)
        initial_data = {
            'first_name': customer.user.first_name,
            'last_name': customer.user.last_name,
            'email': customer.user.email,
            'work_phone': customer.work_phone,
            'home_phone': customer.home_phone
        }
        info_form = CustomerInfoForm(initial_data)
        daddress = DeleteAddressForm()
        context = {
            'customer': customer,
            'info_form': info_form,
            'caddress': caddress,
            'daddress': daddress
        }
        user = self.udao.get_byid(user_id)
        context['username'] = user.username
        context['user_id'] = user.id
        return render(request,self.template_name,context)
    def post(self,request,user_id):
        info_form = CustomerInfoForm(request.POST)
        daddress = DeleteAddressForm(request.POST)
        customer = self.cdao.get_byid(user_id)
        context = {
            'customer': customer
        }
        if 'edit-info' in request.POST:
            if info_form.is_valid():
                updateinfo = CustomerInfo()
                u = User()
                updateinfo.customer_id = user_id
                updateinfo.home_phone = info_form.cleaned_data['home_phone']
                updateinfo.work_phone = info_form.cleaned_data['work_phone']
                u.first_name = info_form.cleaned_data['first_name']
                u.last_name = info_form.cleaned_data['last_name']
                u.email = info_form.cleaned_data['email']
                updateinfo.set_user(u)
                self.cdao.update(updateinfo)
                request.session['user_id'] = user_id
                request.session['username'] = self.cdao.get_byid(user_id).user.username
                context['user_id'] = request.session['user_id'],
                context['username'] = request.session['username'] 
        if 'delete-address' in request.POST:
            if daddress.is_valid():
                a = CustomerAddress()
                a.address_id = daddress.cleaned_data['address_id']
                a.customer_id = user_id
                self.cadao.delete(a)
                request.session['user_id'] = user_id
                request.session['username'] = self.cdao.get_byid(user_id).user.username
                context['user_id'] = request.session['user_id'],
                context['username'] = request.session['username'] 
        return render(request,self.template_name,context)
 
        