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
from django.conf import settings
from django.contrib.auth.hashers import check_password, BCryptPasswordHasher,make_password
from Store.forms import *
from bcrypt import *
#this method will regenerate the new information from the database from post requests
def reCaccount(user_id):
    udao = UserDao()
    pdao = PaymentInfoDao()
    cdao = CustomerInfoDAO()
    cadao = CustomerAddressDao()
    context = {}
    
    user = udao.get_byid(user_id)
    customer = cdao.get_byid(user_id)
    caddress = cadao.get_all_addresses_by_customer_id(user_id)
    p = PaymentInfo()
    p.customer_id = user_id
    payment = pdao.get_all(p)
    initial_data = {
        'first_name': customer.user.first_name,
        'last_name': customer.user.last_name,
        'email': customer.user.email,
        'work_phone': customer.work_phone,
        'home_phone': customer.home_phone
    }
    info_form = CustomerInfoForm(initial_data)
    daddress = DeleteAddressForm()
    aaddress = AddAddressForm()
    eaddress = EditAddressForm()
    Cuserpass = ChangeUsernamePassword()
    context = {
        'customer': customer,
        'info_form': info_form,
        'caddress': caddress,
        'daddress': daddress,
        'aaddress': aaddress,
        'eaddress': eaddress,
        'payment': payment,
        'Cuserpass':Cuserpass 
    }
    user = udao.get_byid(user_id)
    
    return(context)       


class AdminIndexView(TemplateView):
    template_name = 'Store/admin/index.html'
    def get(self,request):
        return render(request,self.template_name,context=None)


class AdminCustomerView(TemplateView):
    template_name = 'Store/admin/customers/customers.html'
    
    def get(self,request):
        cdao = CustomerInfoDAO()

        customers = cdao.get_all()
        context = {
            'customers': customers
        }
        user_id =  request.session['user_id'] 
        username = request.session['username'] 
        context['user_id'] = request.session['user_id'],
        context['username'] = request.session['username'] 
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


class AdminInventoryView(TemplateView):
    template_name = 'Store/admin/inventory/inventory.html'
    idao = InventoryDao()

    def get(self,request):
        inventory = self.idao.get_all()
        context={
            'inventory': inventory
        }
        user_id =  request.session['user_id'] 
        username = request.session['username'] 
        context['user_id'] = request.session['user_id'],
        context['username'] = request.session['username'] 
        return render(request, self.template_name, context)


class CustomerIndexView(TemplateView):
    template_name = 'Store/customer/index.html'
    cus_account = 'Store/customer/customeraccount.hmtl'
    user = User()
    udao = UserDao()

    def get(self,request):
        context = {}
        context['user_id'] = request.session['user_id'],
        context['username'] = request.session['username'] 
        return render(request, self.template_name,context)

    def post(self,request):
        context = {}
        user_id =  request.session['user_id'] 
        user = self.udao.get_byid(user_id)
        request.session['user_id'] = user.id
        request.session['username'] = user.username
        context['user_id'] = request.session['user_id'],
        context['username'] = request.session['username'] 
        return render(request, self.cus_account,context) 

    
class CustomerAccountView(TemplateView):
    template_name = 'Store/customer/customeraccount.html'
    template_name2 = 'Store/customer/caddressaccount.html'
    user = User()
    udao = UserDao()
    customer = CustomerInfo()
    cdao = CustomerInfoDAO()
    cusadd = CustomerAddress()
    cadao = CustomerAddressDao()
    payment = PaymentInfo()
    pdao = PaymentInfoDao()
    def get(self,request):
        user_id = request.session['user_id']
        username = request.session['username'] 
        user = self.udao.get_byid(user_id)
        customer = self.cdao.get_byid(user_id)
        caddress = self.cadao.get_all_addresses_by_customer_id(user_id)
        payment = self.pdao.get_by_customer_id(user_id)
        initial_data = {
            'first_name': customer.user.first_name,
            'last_name': customer.user.last_name,
            'email': customer.user.email,
            'work_phone': customer.work_phone,
            'home_phone': customer.home_phone
        }
        info_form = CustomerInfoForm(initial_data)
        daddress = DeleteAddressForm()
        aaddress = AddAddressForm()
        eaddress = EditAddressForm()
        Cuserpass = ChangeUsernamePassword()
        context = {
            'customer': customer,
            'info_form': info_form,
            'caddress': caddress,
            'daddress': daddress,
            'aaddress': aaddress,
            'eaddress': eaddress,
            'payment': payment,
            'Cuserpass': Cuserpass 
        }
        user = self.udao.get_byid(user_id)
        context['user_id'] = request.session['user_id'],
        context['username'] = request.session['username']
        
        return render(request,self.template_name,context)

    def post(self,request):
        user_id = request.session['user_id']
        username = request.session['username'] 
        info_form = CustomerInfoForm(request.POST)
        daddress = DeleteAddressForm(request.POST)
        aaddress = AddAddressForm(request.POST)
        Cuserpass = ChangeUsernamePassword(request.POST)
        context = {}
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
                context = reCaccount(user_id)
                context['user_id'] = request.session['user_id'],
                context['username'] = request.session['username']
                return render(request, self.template_name, context)
  
        if 'add-address' in request.POST:
            if aaddress.is_valid():
                a = CustomerAddress()
                a.customer_id = user_id
                a.street = aaddress.cleaned_data['street']
                a.city = aaddress.cleaned_data['city']
                a.state_code = aaddress.cleaned_data['state_code']
                a.zip_code = aaddress.cleaned_data['zip_code']
                a.address_type = aaddress.cleaned_data['address_type']
                self.cadao.create(a)
                context = reCaccount(user_id)
                context['user_id'] = request.session['user_id'],
                context['username'] = request.session['username'] 
                return render(request, self.template_name, context)
        
        if 'address-detail' in request.POST:
            context['user_id'] = request.session['user_id'],
            context['username'] = request.session['username'] 
            return render(request,self.template_name2, context)
        
        if 'changeusernamepassword' in request.POST:
            if Cuserpass.is_valid():
                u = User()
                u.id = user_id
                u.username = Cuserpass.cleaned_data['username']
                current_password = Cuserpass.cleaned_data['password']
                # if check_password(current_password, user.password):
                    
        return redirect('customeraccount')


class CAddressAccountView(TemplateView):
    udao = UserDao()
    user = User()
    cadao = CustomerAddressDao()
    customer = CustomerAddress()
    padao = PaymentInfoDao()
    template_name = 'Store/customer/caddressaccount.html' 

    def get(self,request,address_id):
        user_id = request.session['user_id']
        username = request.session['username'] 

        address = self.cadao.get_byid(address_id)
        payment = self.padao.get_by_address_id(address_id, user_id) 

        initial_data = {
            'street': address.street,
            'city': address.city,
            'state_code': address.state_code,
            'zip_code': address.zip_code,
            'address_type': address.address_type
        }

        eaddress = EditAddressForm(initial_data)
        apayment = AddPaymentInfoForm()
        context = {
            'address':address,
            'eaddress': eaddress,
            'payment': payment,
            'apayment': apayment
        }
        user = self.udao.get_byid(user_id)
        context['username'] = user.username
        context['user_id'] = user.id
        return render(request,self.template_name,context) 

    def post(self,request,address_id):
        eaddress = EditAddressForm(request.POST)
        apayment = AddPaymentInfoForm(request.POST)
        address = self.cadao.get_byid(address_id)
        user_id = address.customer_id
         
        if 'edit-address' in request.POST:
            if eaddress.is_valid():
                a = CustomerAddress()
                a.address_id = address_id
                a.customer_id = user_id
                a.street = eaddress.cleaned_data['street']
                a.city = eaddress.cleaned_data['city']
                a.state_code = eaddress.cleaned_data['state_code']
                a.zip_code = eaddress.cleaned_data['zip_code']
                a.address_type = eaddress.cleaned_data['address_type']
                self.cadao.update(a)
                address = self.cadao.get_byid(address_id)
                context = {
                    'address':address,
                    'eaddress': eaddress,
                    # 'payment': payment,
                    'apayment': apayment
                }
                user = self.udao.get_byid(user_id)
                context['username'] = user.username
                context['user_id'] = user.id

        elif 'add-card' in request.POST:
            if apayment.is_valid():
                p = PaymentInfo()
                p.card_number = apayment.cleaned_data['card_number']
                p.cvc = apayment.cleaned_data['cvc']
                p.expir_date = apayment.cleaned_data['expir_date']  
                p.card_issuer = apayment.cleaned_data['card_issuer']
                p.customer_id = user_id
                p.billing_address_id = address_id
                self.padao.create(p)
                address = self.cadao.get_byid(address_id)
                payment = self.padao.get_byid(p)
                context = {
                    'address':address,
                    'eaddress': eaddress,
                    'payment': payment,
                    'apayment': apayment
                }
                user = self.udao.get_byid(user_id)
                context['username'] = user.username
                context['user_id'] = user.id
        return render(request,self.template_name,context) 


class CustomerAddCardView(TemplateView):
    template_name = 'Store/customer/addcard.html'
    user = User()
    udao = UserDao()
    customer = CustomerInfo()
    cdao = CustomerInfoDAO()
    cusadd = CustomerAddress()
    cadao = CustomerAddressDao()
    payment = PaymentInfo()
    pdao = PaymentInfoDao()

    def get(self,request):
        user_id =  request.session['user_id'] 
        username = request.session['username'] 
        user = self.udao.get_byid(user_id)
        customer = self.cdao.get_byid(user_id)
        cusadd =CustomerAddress()
        cusadd.customer_id = user_id
        cusadd.address_type = 'Billing' 
        caddress = self.cadao.get_all_addresses_by_customer_id(user_id)
        addcard = AddPaymentInfoForm()
        bill_add = self.cadao.getBillingAddresses(cusadd)
        billingAddress = BillingAddressesForm(bill_add)
        context = {
            'addcard':addcard,
            'billingAddress':billingAddress
        }
        context['user_id'] = request.session['user_id'],
        context['username'] = request.session['username'] 
        return render(request, self.template_name,context)

    def post(self,request):
        context={}
        user_id = request.session['user_id']
        username = request.session['username'] 
        if 'go-back' in request.POST:
            context['user_id'] = request.session['user_id'],
            context['username'] = request.session['username'] 
            return redirect(reverse('customeraccount'))
        else:
            return render(request,self.template_name,context)
