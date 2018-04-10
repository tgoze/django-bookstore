from django.shortcuts import render
from django.views.generic import TemplateView

from Store.Model.book import Book
from Store.Model.book_dao import BookDao
from Store.Model.author import Author
from Store.Model.publisher import Publisher
from Store.Model.genre import Genre
from .forms import *


def index(request): 
    return render(request, 'Store/index.html')

class AdminBookView(TemplateView):
    template_name = 'Store/admin/books/books.html'
    book_dao = BookDao()
    
    def get(self, request):
        form = BookForm()
        books = self.book_dao.get_all()

        context = {
            'notification': "Please enter book data.",
            'books': books,
            'form': form
        }

        return render(request, self.template_name, context)

    def post(self, request):    
        form = BookForm(request.POST)
        books = self.book_dao.get_all()
        book = Book()
        
        if 'create-book' in request.POST:
            if form.is_valid():
                book.title = form.cleaned_data['title']
                book.isbn10 = form.cleaned_data['isbn10']
                book.isbn13 = form.cleaned_data['isbn13']
                book.copyRightDate = form.cleaned_data['copyright_date']
                book.edition = form.cleaned_data['edition']
                book.numberOfPages = form.cleaned_data['num_pages']
                book.type = form.cleaned_data['book_type']
                author = Author()
                author.author_id = int(form.cleaned_data['authors'])
                book.author = author
                publisher = Publisher()
                publisher.publisher_id = int(form.cleaned_data['publishers'])
                book.publisher = publisher
                genre = Genre()
                genre.genre_id = int(form.cleaned_data['genres'])
                book.genre = genre
                book.image_id = 1

                self.book_dao.create(book)

                context = {
                    'notification': "Book saved successfully!",
                    'books': books,
                    'form': form
                }
            else:
                context = {
                    'notification': "Not a valid submission."
                }

            return render(request, self.template_name, context)

        elif 'edit-book' in request.POST:
            book_id = int(request.POST.get('edit-book'))
            book = self.book_dao.get_byid(book_id)


        elif 'delete-book' in request.POST:
            book_id = int(request.POST.get('delete-book'))
            self.book_dao.delete(book_id)

            context = {                
                'books': books,
                'form': form
            }

            return render(request, self.template_name, context)


class AdminBookDetailView(TemplateView):
    template_name = 'Store/admin/books/details.html'
    book_dao = BookDao()
    
    def get(self, request, bookID):
        book = self.book_dao.get_byid(bookID)
    
        context = {
            'book': book
        }

        return render(request, 'Store/admin/books/details.html', context)

    def post(self, request):
        book = self.book_dao.get_byid(bookID)
    
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
