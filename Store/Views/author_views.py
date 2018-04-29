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

class AdminAuthorView(TemplateView):
    template_name = 'Store/admin/authors/authors.html'
    adao = AuthorDao()
   
    @never_cache
    def get(self,request):
        authors = self.adao.get_all()
        aauthor = AuthorForm()
        
        context = {
            'authors': authors,
            'aauthor': aauthor
        }
        
        user_id =  request.session['user_id'] 
        username = request.session['username'] 
        context['user_id'] = request.session['user_id']
        context['username'] = request.session['username']
        return render(request,self.template_name, context) 
    
    @never_cache
    def post(self,request):
        user_id =  request.session['user_id'] 
        username = request.session['username'] 
        aauthor = AuthorForm(request.POST)
        context = {}
        if 'create-author' in request.POST:
            if aauthor.is_valid():
                a = Author()
                a.first_name = aauthor.cleaned_data['first_name']
                a.last_name = aauthor.cleaned_data['last_name']
                self.adao.create(a)
                context['user_id'] = request.session['user_id']
                context['username'] = request.session['username']  
            return redirect(reverse('adminauthorindex')) 
    
class AdminAuthorDetailView(TemplateView):
    template_name = 'Store/admin/authors/details.html'
    adao = AuthorDao()
    bdao = BookDao()
    idao = InventoryDao()
    @never_cache
    def get(self,request,author_id):
        author = self.adao.get_byid(author_id)
        books = self.idao.getInventoryByAuthor(author_id)
        initial_data = {
            'first_name': author.first_name,
            'last_name': author.last_name
        }
        eauthor = AuthorForm(initial_data)
        context = {
            'author': author,
            'books': books,
            'eauthor': eauthor,
            'sum': self.adao.getTotalAuthorRevenueByAuthorID(author_id),
            'sum_inventory': self.adao.getTotalInventoryByAuthorID(author_id)
        }
        user_id =  request.session['user_id'] 
        username = request.session['username'] 
        context['user_id'] = request.session['user_id']
        context['username'] = request.session['username']
        
        return render(request,self.template_name,context)
    
    @never_cache
    def post(self,request,author_id):
        user_id =  request.session['user_id'] 
        username = request.session['username'] 
        context = {}
        eauthor = AuthorForm(request.POST)
        if 'update-author' in  request.POST:
            if eauthor.is_valid():
                a = Author()
                a.author_id = author_id
                a.first_name = eauthor.cleaned_data['first_name']
                a.last_name = eauthor.cleaned_data['last_name']
                self.adao.update(a)
                context['user_id'] = request.session['user_id']
                context['username'] = request.session['username']
            return redirect(reverse(('adminauthordetail'),kwargs={ 'author_id': author_id }))
        if 'delete-author' in request.POST:
            self.adao.delete(author_id)
            context['user_id'] = request.session['user_id']
            context['username'] = request.session['username']
            return redirect(reverse('adminauthorindex'))
