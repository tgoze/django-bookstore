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

class AdminPublisherIndexView(TemplateView):
    template_name = 'Store/admin/publishers/publishers.html'
    pdao = PublisherDao()

    @never_cache
    def get(self,request):
        publishers = self.pdao.get_all()
        apublisher = PublisherForm()
        context = {
            'publishers':publishers,
            'apublisher': apublisher
        }
        user_id =  request.session['user_id'] 
        username = request.session['username'] 
        context['user_id'] = request.session['user_id'],
        context['username'] = request.session['username'] 
        return render(request, self.template_name, context)
    @never_cache
    def post(self,request):
        user_id =  request.session['user_id'] 
        username = request.session['username']
        context = {}
        apublisher = PublisherForm(request.POST)
        if 'create-publisher' in request.POST:
            if apublisher.is_valid():
                p = Publisher()
                p.company_name = apublisher.cleaned_data['company_name']
                p.city = apublisher.cleaned_data['city']
                p.state_code = apublisher.cleaned_data['state_code']
                p.zip_code = apublisher.cleaned_data['zip_code']
                p.phone_number = apublisher.cleaned_data['phone_number']
                p.contact_name = apublisher.cleaned_data['contact_name']
                self.pdao.create(p)
            context['user_id'] = request.session['user_id'],
            context['username'] = request.session['username'] 
            return redirect(reverse('adminpublisherindex'))

class AdminPublisherDetailView(TemplateView):
    template_name = 'Store/admin/publishers/details.html'
    pdao = PublisherDao()
    bdao = BookDao()
    idao = InventoryDao()
    @never_cache
    def get(self,request, publisher_id):
        publisher = self.pdao.get_byid(publisher_id)
        books = self.idao.getInventoryByPublisher(publisher_id)

        initial_data = {
            'company_name': publisher.company_name,
            'city': publisher.city,
            'state_code': publisher.state_code,
            'zip_code': publisher.zip_code,
            'phone_number': publisher.phone_number,
            'contact_name': publisher.contact_name
        }
        epublisher = PublisherForm(initial_data)
        context ={
            'publisher': publisher,
            'books': books,
            'epublisher': epublisher,
            'sum':self.pdao.getTotalPublisherRevenueByPublisherID(publisher_id),
            'sum_inventory': self.pdao.getTotalInventoryByPublisherID(publisher_id)
        }
        user_id =  request.session['user_id'] 
        username = request.session['username'] 
        context['user_id'] = request.session['user_id'],
        context['username'] = request.session['username'] 
        return render(request, self.template_name, context)
    
    @never_cache
    def post(self,request,publisher_id):
        user_id =  request.session['user_id'] 
        username = request.session['username'] 
        context = {}
        epublisher = PublisherForm (request.POST)

        if 'update-publisher' in request.POST:
            if epublisher.is_valid():
                p = Publisher()
                p.company_name = epublisher.cleaned_data['company_name']
                p.city = epublisher.cleaned_data['city']
                p.state_code = epublisher.cleaned_data['state_code']
                p.zip_code = epublisher.cleaned_data['zip_code']
                p.phone_number = epublisher.cleaned_data['phone_number']
                p.contact_name = epublisher.cleaned_data['contact_name']
                p.publisher_id = publisher_id
                self.pdao.update(p)
                context['user_id'] = request.session['user_id'],
                context['username'] = request.session['username'] 
            return redirect(reverse(('adminpublisherdetail'),kwargs={ 'publisher_id': publisher_id }))

        if 'delete-publisher' in request.POST:
            self.pdao.delete(publisher_id)
            context['user_id'] = request.session['user_id'],
            context['username'] = request.session['username'] 
            return redirect(reverse('adminpublisherindex'))
