from django.shortcuts import render
from django.views.generic import TemplateView
from Store.Model.user import User
from Store.Model.user_dao import UserDao
from Store.Model.customer_info import CustomerInfo
from Store.Model.customer_info_dao import CustomerInfoDAO
from Store.Model.customer_address import CustomerAddress
from django.conf import settings
from django.contrib.auth.hashers import check_password, BCryptPasswordHasher,make_password

from Store.forms import *
from bcrypt import *


class HomeView(TemplateView):
    template_name = 'Store/index.html'
    def get(self, request):
        return render(request, self.template_name)
        
class LoginView(TemplateView):
    user = User()
    udao = UserDao()
    template_name = 'Store/login.html'
    cus_loggedin_template = 'Store/customer/index.html' #this html needs made
    admin_loggedin_template = 'Store/admin/index.html' #this html needs made
    user.username = 'not logged in'
    customer = CustomerInfo()
    cdao = CustomerInfoDAO()
    def get(self, request):  
        loginform = LoginForm()  
        registerform = RegisterUserForm()
        context = {
            'loginform': loginform,
            'registerform': registerform           
        }

        return render(request, self.template_name, context)

    def post(self, request):
        #settings.configure(DEBUG=True)
        loginform = LoginForm(request.POST)
        registerform = RegisterUserForm(request.POST)

        context = {
            'user_id': None
        }

        if 'login-user' in request.POST:
            if loginform.is_valid():     
                user = User()           
                user.username = loginform.cleaned_data['username']
                user = self.udao.get_byusername(user.username)
                input_password = loginform.cleaned_data['password']                
                if check_password(input_password, user.password):
                    request.session['user_id'] = user.id
                    request.session['username'] = user.username
                    context['text'] = 'Yay password'                
                    context['user_id'] = request.session['user_id']
                    context['username'] = request.session['username']                    
                    self.udao.updateLastLogin(user.id)
                    if user.is_staff == 0:
                        self.template_name = self.cus_loggedin_template
                    else:
                        self.template_name = self.admin_loggedin_template
                else:
                    context['text'] = 'Bad password bro'
                        
            else:
                context['text'] = 'try again'

        if 'create-user' in request.POST:        
            if registerform.is_valid():
                user = User()
                user.first_name = registerform.cleaned_data['first_name']
                user.last_name = registerform.cleaned_data['last_name']
                user.email = registerform.cleaned_data['email']
                user.username = registerform.cleaned_data['username']
                x = registerform.cleaned_data['password']
                user.is_superuser = 0
                user.is_active = 1
                user.is_staff = 0
                user.password = make_password(x,salt=None,hasher='default')
                self.udao.create(user)
                user = self.udao.get_byusername(user.username)  
                customer = CustomerInfo()
                customer.customer_id = user.id
                customer.work_phone = registerform.cleaned_data['work_phone']
                customer.home_phone = registerform.cleaned_data['home_phone']
                self.cdao.create(customer)
                request.session['user_id'] = user.id
                request.session['username'] = user.username 
                context['user_id'] = request.session['user_id']
                context['username'] = request.session['username']   
                self.template_name = self.cus_loggedin_template     
            context = {
                    'loginform': loginform,
                    'registerform': registerform           
                }                  
        return render(request, self.template_name, context)