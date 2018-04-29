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

class AdminGenreIndexView(TemplateView):
    template_name = 'Store/admin/genres/genres.html'
    gdao = GenreDao()
    udao = UserDao()
    @never_cache
    def get(self,request):
        genres = self.gdao.get_all()
        agenre = GenreForm()
        context = {
            'genres':genres,
            'agenre': agenre
 
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
        agenre = GenreForm(request.POST)
        context = {}
        if 'create-genre' in request.POST:
            if agenre.is_valid():
                genre = Genre()
                genre.genre = agenre.cleaned_data['genre']                
                self.gdao.create(genre) 
                context['user_id'] = request.session['user_id'],
                context['username'] = request.session['username'] 
                return redirect(reverse('admingenreindex'))
        else: 
            return redirect(reverse('adminindex'))

class AdminGenreDetailsView(TemplateView):
    template_name = 'Store/admin/genres/details.html'
    gdao = GenreDao()
    udao = UserDao()
    bdao = BookDao()
    idao = InventoryDao()
    @never_cache
    def get(self,request,genre_id):

        genre = self.gdao.get_byid(genre_id)
        books = self.idao.getInventoryByGenre(genre_id)
        sum_inventory = self.gdao.getTotalInventoryByGenreID(genre_id)

        initial_data = {
            'genre':genre.genre 
        }
        egenre = GenreForm(initial_data)
        context = {
            'genre':genre,
            'books': books,
            'egenre': egenre,
            'sum': self.gdao.getTotalGenreRevenueByGenreID(genre_id),
            'sum_inventory':sum_inventory
        }
        
        user_id =  request.session['user_id'] 
        username = request.session['username'] 
        context['user_id'] = request.session['user_id'],
        context['username'] = request.session['username'] 
        return render(request, self.template_name, context)
    
    def post(self,request,genre_id):
        user_id =  request.session['user_id'] 
        username = request.session['username'] 
        egenre = GenreForm(request.POST)
        context = {}
        if 'update-genre' in request.POST:
            if egenre.is_valid():
                g = Genre()
                g.genre = egenre.cleaned_data['genre']
                g.genre_id = genre_id
                self.gdao.update(g)
                context['user_id'] = request.session['user_id'],
                context['username'] = request.session['username'] 
                return redirect(reverse(('admingenredetail'),kwargs={ 'genre_id': genre_id }))

        elif 'delete-genre' in request.POST:
            g = Genre()
            g.genre_id = genre_id
            self.gdao.delete(g)
            context['user_id'] = request.session['user_id'],
            context['username'] = request.session['username']
            return redirect(reverse('admingenreindex')) 

        else:
            return redirect(reverse(('admingenredetail'),kwargs={ 'genre_id': genre_id }))


                