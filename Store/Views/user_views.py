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


def admin_customer_details(request,customer_id):
    cdao = CustomerInfoDAO()

    customer = cdao.get_byid(customer_id)
    customer_address = cdao.get_addressbyid(customer_id)
    context = {
        'customer': customer,
        'caddress': customer_address
    }
    return render(request,'Store/admin/customers/details.html', context)


class LoginView(TemplateView):
    user = User()
    udao = UserDao()
    login_template = 'Store/customer/login.html'
    loggedin_template = 'Store/customer/test.html'
    user.username = 'not logged in'

    def get(self, request):  
        loginform = LoginForm()  
        registerform = RegisterUserForm()
        context = {
            'loginform': loginform,
            'registerform': registerform           
        }

        return render(request, self.login_template, context)

    def post(self, request):
        #settings.configure(DEBUG=True)
        user = User()
        udao = UserDao()

        login_form = LoginForm(request.POST)
        register_form = RegisterUserForm(request.POST)

        if 'login-user' in request.POST:
            if login_form.is_valid():
                user.username = login_form.cleaned_data['username']
                user.password = login_form.cleaned_data['password']
                user.id = udao.get_byusername(user.username).id
                if check_password(user.password,udao.get_byusername(user.username).password):
                    request.session['user_id'] = user.id
                    request.session['username'] = user.username
                    context = {
                        'text': 'Yay password',
                        'user_id': request.session['user_id'],
                        'username': request.session['username']
                    }                    
                else:
                    context = {
                        'text': 'Bad password bro',
                        'user_id': None
                    }    
            else:
                context = {
                    'text': 'try again',
                    'user_id': None
                }

            return render(request, self.loggedin_template, context)

        if 'create-user' in request.POST:        
            if register_form.is_valid():
                user.first_name = register_form.cleaned_data['first_name']
                user.last_name = register_form.cleaned_data['last_name']
                user.email = register_form.cleaned_data['last_name']
                user.username = register_form.cleaned_data['username']
                x = register_form.cleaned_data['password']
                user.is_superuser = 0
                user.is_active = 1
                user.is_staff = 0
                user.password = make_password(x,salt=None,hasher='default')
                udao.create(user)
                context = {
                    'text': 'user saved???'            
                }
            else:
                context = {
                    'text': 'try again'                    
                }
                
            return render(request,self.login_template, context)