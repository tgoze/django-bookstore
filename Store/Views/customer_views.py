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
from django.views.decorators.cache import never_cache




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
    @never_cache 
    def get(self,request):
        user = User()
        udao = UserDao()
        customer = CustomerInfo()
        cdao = CustomerInfoDAO()
        cusadd = CustomerAddress()
        cadao = CustomerAddressDao()
        payment = PaymentInfo()
        pdao = PaymentInfoDao()
        user_id = request.session['user_id']
        username = request.session['username'] 
        user = udao.get_byid(user_id)
        customer = cdao.get_byid(user_id)
        caddress = cadao.get_all_addresses_by_customer_id(user_id)
        payment = pdao.get_by_customer_id(user_id)
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
        user = udao.get_byid(user_id)
        
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
            return rendr(request,self.template_name2, context)
        
        if 'changeusernamepassword' in request.POST:
            if Cuserpass.is_valid():
                u = self.udao.get_byid(user_id)
                u.id = user_id
                u.username = Cuserpass.cleaned_data['username']
                current_password = Cuserpass.cleaned_data['password']
                if check_password(current_password, u.password):
                    x = Cuserpass.cleaned_data['password2']
                    u.password = make_password(x,salt=None,hasher='default')
                    self.udao.updateUserPass(u)
                    context = context = reCaccount(user_id)
                    context['user_id'] = request.session['user_id'],
                    context['username'] = request.session['username'] 
                    return render(request, self.template_name, context)
        elif 'deactivate' in request.POST:
            self.udao.deactivateUser(user_id)
            return redirect(reverse('login'))
        return redirect('customeraccount')


class CAddressAccountView(TemplateView):
    udao = UserDao()
    user = User()
    cadao = CustomerAddressDao()
    customer = CustomerAddress()
    padao = PaymentInfoDao()
    template_name = 'Store/customer/caddressaccount.html' 
    cus_account = 'Store/customer/customeraccount.html'
    def get(self,request,address_id):
        user_id = request.session['user_id']
        username = request.session['username'] 

        address = self.cadao.get_byid(address_id) 
        payment = self.padao.get_by_address_id(address_id,user_id)

        initial_data = {
            'street': address.street,
            'city': address.city,
            'state_code': address.state_code,
            'zip_code': address.zip_code,
            'address_type': address.address_type
        }

        eaddress = EditAddressForm(initial_data)
        daddress = DeleteAddressForm()
        apayment = AddPaymentInfoForm2()
        context = {
            'address':address,
            'eaddress': eaddress,
            'payment': payment,
            'apayment': apayment,
            'daddress': daddress
        }
        user = self.udao.get_byid(user_id)
        context['username'] = user.username
        context['user_id'] = user.id
        return render(request,self.template_name,context) 

    def post(self,request,address_id):
        eaddress = EditAddressForm(request.POST)
        apayment = AddPaymentInfoForm2(request.POST)
        daddress = DeleteAddressForm(request.POST)
        address = self.cadao.get_byid(address_id)
        user_id = address.customer_id
        context = {}
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
                context = recaddress(address_id)
                user = self.udao.get_byid(user_id)
                context['username'] = user.username
                context['user_id'] = user.id
            return render(request,self.template_name,context)

        elif 'add-card' in request.POST:
            if apayment.is_valid():
                p = PaymentInfo()
                p.card_number = apayment.cleaned_data['card_number']
                p.cvc = apayment.cleaned_data['cvc']
                p.expir_date = apayment.cleaned_data['expir_date']  
                p.card_issuer = apayment.cleaned_data['card_issuer']
                p.customer_id = user_id
                p.billing_address.address_id = address_id
                self.padao.create(p)
                context = recaddress(address_id)
                user = self.udao.get_byid(user_id)
                context['username'] = user.username
                context['user_id'] = user.id
            return render(request,self.template_name,context)

        elif 'delete-address' in request.POST: 
            if daddress.is_valid():
                a = CustomerAddress()
                a.address_id = daddress.cleaned_data['address_id']
                a.customer_id = user_id
                self.cadao.delete(a)
                context = reCaccount(user_id)
                user = self.udao.get_byid(user_id)
                context['username'] = user.username
                context['user_id'] = user.id
            return redirect(reverse('customeraccount')) 
        elif 'go-back' in request.POST:
            user = self.udao.get_byid(user_id)
            context = reCaccount(user_id)
            context['username'] = user.username
            context['user_id'] = user.id
            return redirect(reverse('customeraccount'))

class CustomerCardView(TemplateView):
    template_name = 'Store/customer/ccard.html'
    udao = UserDao()
    pdao = PaymentInfoDao()
    def get(self,request,card_id):
        user_id = request.session['user_id']
        username = request.session['username'] 
        user = self.udao.get_byid(user_id)
        card = self.pdao.get_byid(card_id)
        context = {
            'card': card
        }
        context['username'] = user.username
        context['user_id'] = user.id
        return render(request, self.template_name, context)

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
        context={}
        user_id =  request.session['user_id'] 
        username = request.session['username'] 
        user = self.udao.get_byid(user_id)
        customer = self.cdao.get_byid(user_id)
        cusadd =CustomerAddress()
        cusadd.customer_id = user_id
        caddress = self.cadao.get_all_addresses_by_customer_id(user_id)
        bill_addresses = self.cadao.get_by_customer_and_type(user_id, "Billing")

        bill_address_choices = []
        for address in bill_addresses:
            address_val = (str(address.address_id), str(address.street) + " " + str(address.city) + ", " 
                    + str(address.state_code) + " " + str(address.zip_code))
            bill_address_choices.append(address_val)
        aaddress = AddAddressForm2()
        addcard = AddPaymentInfoForm(bill_address_choices=bill_address_choices)
        context['addcard'] = addcard
        context['aaddress'] = aaddress
        context['user_id'] = request.session['user_id']
        context['username'] = request.session['username'] 
        return render(request, self.template_name,context)

    def post(self,request):
        context={}
        user_id = request.session['user_id']
        username = request.session['username'] 
        bill_addresses = self.cadao.get_by_customer_and_type(user_id, "Billing")
        bill_address_choices = []
        for address in bill_addresses:
            address_val = (str(address.address_id), str(address.street) + " " + str(address.city) + ", " 
                    + str(address.state_code) + " " + str(address.zip_code))
            bill_address_choices.append(address_val)
        addcard = AddPaymentInfoForm(request.POST,bill_address_choices=bill_address_choices)
        aaddress = AddAddressForm2(request.POST)

        if 'go-back' in request.POST:
            context['user_id'] = request.session['user_id']
            context['username'] = request.session['username'] 
            return redirect(reverse('customeraccount'))

        elif 'add-card' in request.POST:
            if addcard.is_valid():
                p = PaymentInfo()
                p.customer_id = user_id 
                p.card_number = addcard.cleaned_data['card_number']
                p.cvc = addcard.cleaned_data['cvc']
                p.expir_date = addcard.cleaned_data['expir_date']
                p.card_issuer = addcard.cleaned_data['card_issuer']
                p.billing_address.address_id = addcard.cleaned_data['billing_addresses']
                self.pdao.create(p)
                context['user_id'] = request.session['user_id'],
                context['username'] = request.session['username'] 
            return redirect(reverse('customeraccount'))

        elif 'add-address' in request.POST:
            if aaddress.is_valid():
                a = CustomerAddress()
                a.customer_id = user_id
                a.street = aaddress.cleaned_data['street']
                a.city = aaddress.cleaned_data['city']
                a.state_code = aaddress.cleaned_data['state_code']
                a.zip_code = aaddress.cleaned_data['zip_code']
                a.address_type = 'Billing'
                self.cadao.create(a)
                user = self.udao.get_byid(user_id)
                customer = self.cdao.get_byid(user_id)
                cusadd =CustomerAddress()
                cusadd.customer_id = user_id
                caddress = self.cadao.get_all_addresses_by_customer_id(user_id)
                bill_addresses = self.cadao.get_by_customer_and_type(user_id, "Billing")

                bill_address_choices = []
                for address in bill_addresses:
                    address_val = (str(address.address_id), str(address.street) + " " + str(address.city) + ", " 
                            + str(address.state_code) + " " + str(address.zip_code))
                    bill_address_choices.append(address_val)
                aaddress = AddAddressForm2()
                addcard = AddPaymentInfoForm(bill_address_choices=bill_address_choices)
                context['addcard'] = addcard
                context['aaddress'] = aaddress
                context['user_id'] = request.session['user_id']
                context['username'] = request.session['username'] 
            return render(request, self.template_name, context)
        else:
            return render(request,self.template_name,context)
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
    payment = pdao.get_by_customer_id(user_id)
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

def recaddress( address_id):
    udao = UserDao()
    pdao = PaymentInfoDao()
    cdao = CustomerInfoDAO()
    cadao = CustomerAddressDao()
    context = {}
    address = cadao.get_byid(address_id) 
    user_id = address.customer_id
    payment = pdao.get_by_address_id(address_id,user_id)

    initial_data = {
        'street': address.street,
        'city': address.city,
        'state_code': address.state_code,
        'zip_code': address.zip_code,
        'address_type': address.address_type
    }

    eaddress = EditAddressForm(initial_data)
    apayment = AddPaymentInfoForm2()
    daddress = DeleteAddressForm()
    context = {
        'address':address,
        'eaddress': eaddress,
        'payment': payment,
        'apayment': apayment,
        'daddress': daddress
    }
    user = udao.get_byid(user_id)
    return(context)