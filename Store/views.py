from django.shortcuts import render
from Store.Model.book_dao import BookDao

# Create your views here.
def index(request): 
    return render(request, 'Store/index.html')

def admin_books(request):

    book_dao = BookDao()
    books = book_dao.get_all()

    context = {
        'title': 'Books',
        'books': books
    }

    return render(request, 'Store/admin/books/books.html', context)

def admin_book_details(request, bookID):
    
    book_dao = BookDao()
    book = book_dao.get_byid(bookID)

    context = {
        'book': book
    }

    return render(request, 'Store/admin/books/details.html', context)