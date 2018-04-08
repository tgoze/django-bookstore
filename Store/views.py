from django.shortcuts import render
from Store.Model.book_dao import BookDao
from Store.Model.publisher_dao import PublisherDao
from Store.Model.genre_dao import GenreDao
from Store.Model.customer_info_dao import CustomerInfoDAO
from Store.forms import BookForm

# Create your views here.
def index(request): 
    return render(request, 'Store/index.html')

def admin_books(request):

    book_dao = BookDao()
    publisher_dao = PublisherDao()
    genre_dao = GenreDao()

    books = book_dao.get_all()
    publishers = publisher_dao.get_all()
    genres = genre_dao.get_all()

    context = {
        'title': 'Books',
        'books': books,
        'publishers': publishers,
        'genres': genres
    }

    return render(request, 'Store/admin/books/books.html', context)

def admin_book_details(request, bookID):
    
    book_dao = BookDao()

    book = book_dao.get_byid(bookID)

    context = {
        'book': book
    }

    return render(request, 'Store/admin/books/details.html', context)

def admin_customers(request):
    customer_info_dao = CustomerInfoDAO()

    customers = customer_info_dao.get_all()
    context = {
        'customers':customers
    }
    return render(request, 'Store/admin/customers/customers.html', context)
