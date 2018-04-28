from django.shortcuts import render, redirect, reverse
from django.views.generic import TemplateView
from Store.Model.user import User
from Store.Model.user_dao import UserDao
from Store.Model.customer_info import CustomerInfo
from Store.Model.customer_info_dao import CustomerInfoDAO
from Store.Model.customer_address import CustomerAddress
from django.conf import settings
from django.contrib.auth.hashers import check_password, BCryptPasswordHasher,make_password

from django.views.decorators.cache import never_cache

from Store.forms import *
from bcrypt import *


class HomeView(TemplateView):
    template_name = 'Store/index.html'
    @never_cache
    def get(self, request):
        context = {}
        context['user_id'] = request.session['user_id']
        return render(request, self.template_name, context)
        
class LoginView(TemplateView):
    user = User()
    udao = UserDao()
    template_name = 'Store/login.html'
    cus_loggedin_template = 'Store/customer/index.html' 
    admin_loggedin_template = 'Store/admin/index.html' 
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
                # Get user data from database
                user = User()           
                user.username = loginform.cleaned_data['username']
                user = self.udao.get_byusername(user.username)
                input_password = loginform.cleaned_data['password']
                # Validate login
                if check_password(input_password, user.password):
                    # Store session data
                    request.session['user_id'] = user.id
                    request.session['username'] = user.username
                    request.session['user_is_staff'] = user.is_staff

                    context['text'] = 'Yay password'                
                    context['user_id'] = request.session['user_id']
                    context['username'] = request.session['username']                    
                    self.udao.updateLastLogin(user.id)
                    if user.is_staff == 0 and user.is_active == 1:
                        return redirect(reverse('customer_index'))
                    elif user.is_active == 0 and user.is_staff == 0:
                        self.udao.activateUser(user.id)
                        return redirect(reverse('customer_index'))
                    else:
                        return redirect(reverse('adminindex'))
                                        
                # Handle if password is bad
                else:
                    loginform = LoginForm()  
                    registerform = RegisterUserForm()
                    context = {
                        'loginform': loginform,
                        'registerform': registerform,   
                        'text': 'Either username or password is incorrect'        
                    }          
                    return render(request, self.template_name, context)
                
            else:
                context['text'] = 'try again'
                return render(request, self.template_name, context)

        if 'create-user' in request.POST:        
            if registerform.is_valid():
                u = User()
                u.first_name = registerform.cleaned_data['first_name']
                u.last_name = registerform.cleaned_data['last_name']
                u.email = registerform.cleaned_data['email']
                u.username = registerform.cleaned_data['username']
                x = registerform.cleaned_data['password']
                u.is_superuser = 0
                u.is_active = 1
                u.is_staff = 0
                u.password = make_password(x,salt=None,hasher='default')
                self.udao.create(u)
                user = self.udao.get_byusername(u.username)  
                customer = CustomerInfo()
                customer.customer_id = user.id
                customer.work_phone = registerform.cleaned_data['work_phone']
                customer.home_phone = registerform.cleaned_data['home_phone']
                self.cdao.create(customer)
                loginform = LoginForm()  
                registerform = RegisterUserForm()
                context = {
                    'loginform': loginform,
                    'registerform': registerform           
                }           

                return render(request, self.template_name, context)