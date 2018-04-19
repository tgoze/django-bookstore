from django.shortcuts import render
from django.views.generic import TemplateView
from Store.Model.user import User
from Store.Model.user_dao import UserDao
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
    admin_loggedin_template = 'Store/customer/index.html' #this html needs made
    user.username = 'not logged in'

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
        user = User()
        udao = UserDao()

        login_form = LoginForm(request.POST)
        register_form = RegisterUserForm(request.POST)

        context = {
            'user_id': None
        }

        if 'login-user' in request.POST:
            if login_form.is_valid():                
                user.username = login_form.cleaned_data['username']
                user = udao.get_byusername(user.username)
                input_password = login_form.cleaned_data['password']                
                if check_password(input_password, user.password):
                    request.session['user_id'] = user.id
                    request.session['username'] = user.username
                    context['text'] = 'Yay password'                
                    context['user_id'] = request.session['user_id']
                    context['username'] = request.session['username']                    

                    if user.is_staff == 0:
                        self.template_name = self.cus_loggedin_template
                    else:
                        self.template_name = self.admin_loggedin_template
                else:
                    context['text'] = 'Bad password bro'
                        
            else:
                context['text'] = 'try again'

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
                context['text'] = 'User saved successfully!'            
            else:
                context['text'] = 'Invalid data'                    
                
        return render(request, self.template_name, context)