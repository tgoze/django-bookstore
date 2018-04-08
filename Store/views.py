from django.shortcuts import render
from django.views.generic import TemplateView

from Store.Model.book import Book
from Store.Model.book_dao import BookDao
from Store.Model.author import Author
from Store.Model.publisher import Publisher
from Store.Model.genre import Genre
from .forms import BookForm


def index(request): 
    return render(request, 'Store/index.html')

class AdminBookView(TemplateView):
    template_name = 'Store/admin/books/books.html'

    def get(self, request):
        book_dao = BookDao()
        books = book_dao.get_all()

        form = BookForm()

        context = {
            'title': 'Books',
            'books': books,
            'form': form
        }

        return render(request, self.template_name, context)

    def post(self, request):
        book = Book()
        book_dao = BookDao()
        
        form = BookForm(request.POST)
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

            book_dao.create(book)

            context = {
                'text': "Post successful!"
            }
        else:
            context = {
                'text': "Not valid bro"
            }

        return render(request, self.template_name, context)


def admin_book_details(request, bookID):
    
    book_dao = BookDao()

    book = book_dao.get_byid(bookID)

    context = {
        'book': book
    }

    return render(request, 'Store/admin/books/details.html', context)