from django.shortcuts import render
from django.views.generic import TemplateView
from Store.Model.book import Book
from Store.Model.book_dao import BookDao
from Store.Model.author import Author
from Store.Model.author_dao import AuthorDao
from Store.Model.publisher import Publisher
from Store.Model.publisher_dao import PublisherDao
from Store.Model.genre import Genre
from Store.Model.genre_dao import GenreDao
from Store.Model.inventory import Inventory
from Store.Model.inventory_dao import InventoryDao
from Store.Model.image import Image
from Store.Model.image_dao import ImageDao
from Store.Model.cart import Cart
from Store.Model.cart_dao import CartDao
from Store.forms import BookForm, BookImageForm, AuthorForm, PublisherForm, GenreForm, CartForm

from django.conf import settings
from django.core.files.storage import FileSystemStorage


class AdminBookView(TemplateView):
    template_name = 'Store/admin/books/books.html'
    book_dao = BookDao()
    
    def get(self, request):
        book_form = BookForm()
        publisher_form = PublisherForm()
        author_form = AuthorForm()
        genre_form = GenreForm()
        books = self.book_dao.get_all()

        context = {
            'notification': "Please enter book data.",
            'books': books,
            'book_form': book_form,
            'publisher_form': publisher_form,
            'author_form': author_form,
            'genre_form': genre_form
        }

        return render(request, self.template_name, context)

    def post(self, request):    
        book_form = BookForm(request.POST)
        books = self.book_dao.get_all()
        book = Book()

        publisher_form = PublisherForm(request.POST)
        publisher = Publisher()
        publisher_dao = PublisherDao()

        author_form = AuthorForm(request.POST)
        author = Author()
        author_dao = AuthorDao()

        genre_form = GenreForm(request.POST)
        genre = Genre()
        genre_dao = GenreDao()

        context = {
            'notification': "Please enter book data.",
            'books': books,
            'book_form': book_form,
            'publisher_form': publisher_form,
            'author_form': author_form,
            'genre_form': genre_form
        }
        
        if 'create-book' in request.POST:
            if book_form.is_valid():
                book.title = book_form.cleaned_data['title']
                book.isbn10 = book_form.cleaned_data['isbn10']
                book.isbn13 = book_form.cleaned_data['isbn13']
                book.copyRightDate = book_form.cleaned_data['copyright_date']
                book.edition = book_form.cleaned_data['edition']
                book.numberOfPages = book_form.cleaned_data['num_pages']
                book.type = book_form.cleaned_data['book_type']
                author = Author()
                author.author_id = int(book_form.cleaned_data['authors'])
                book.author = author
                publisher = Publisher()
                publisher.publisher_id = int(book_form.cleaned_data['publishers'])
                book.publisher = publisher
                genre = Genre()
                genre.genre_id = int(book_form.cleaned_data['genres'])
                book.genre = genre                

                self.book_dao.create(book)

                context['notification'] = "Book saved successfully!"
              
            else:
                context['notification'] = "Not a valid submission."                        

        elif 'delete-book' in request.POST:
            book_id = int(request.POST.get('delete-book'))
            self.book_dao.delete(book_id)            
        
        elif 'create-publisher' in request.POST:
            if publisher_form.is_valid():
                publisher.company_name = publisher_form.cleaned_data['company_name']
                publisher.city = publisher_form.cleaned_data['city']
                publisher.state_code = publisher_form.cleaned_data['state_code']
                publisher.zip_code = publisher_form.cleaned_data['zip_code']

                publisher_dao.create(publisher)
                
                context = {
                    'notification': "Publisher saved successfully!",
                    'book_form': book_form
                }
            else:
                context = {
                    'notification': "Not a valid submission.",
                    'book_form': book_form
                }                   
        
        elif 'create-author' in request.POST:
            if author_form.is_valid():
                author.first_name = author_form.cleaned_data['first_name']
                author.last_name = author_form.cleaned_data['last_name']

                author_dao.create(author) 
                
                context = {
                    'notification': "Author saved successfully!",
                    'book_form': book_form
                }
            else:
                context = {
                    'notification': "Not a valid submission.",
                    'book_form': book_form
                }

        elif 'create-genre' in request.POST:
            if genre_form.is_valid():
                genre.genre = genre_form.cleaned_data['genre']                

                genre_dao.create(genre) 
                
                context = {
                    'notification': "Genre saved successfully!",
                    'book_form': book_form
                }
            else:
                context = {
                    'notification': "Not a valid submission.",
                    'book_form': book_form
                }
            
        return render(request, self.template_name, context)


class AdminBookDetailView(TemplateView):
    template_name = 'Store/admin/books/details.html'    
    book_dao = BookDao()
    image_dao = ImageDao()
    inventory_dao = InventoryDao()
    
    def get(self, request, book_id):
        book = self.book_dao.get_byid(book_id)
        images = self.image_dao.get_byid(book_id)
        inventory  = self.inventory_dao.get_byid(book_id)

        initial_data = {
            'title': book.title,
            'authors': book.author.author_id,
            'isbn10': book.isbn10,
            'isbn13': book.isbn13,
            'copyright_date': book.copyRightDate,
            'edition': book.edition,
            'publishers': book.publisher.publisher_id,
            'book_type': book.type,
            'num_pages': book.numberOfPages,
            'genres': book.genre.genre_id
        }
        book_form = BookForm(initial_data)
        image_form = BookImageForm()        

        context = {
            'book': book,
            'images': images,
            'inventory': inventory,
            'book_form': book_form,
            'image_form': image_form
        }

        return render(request, self.template_name, context)

    def post(self, request, book_id):
        book_form = BookForm(request.POST)
        book = self.book_dao.get_byid(book_id)
        
        context = {
            'book': book
        }

        if 'update-book' in request.POST:
            if book_form.is_valid():
                updated_book = Book()
                updated_book.book_id = book_id
                updated_book.title = book_form.cleaned_data['title']
                updated_book.isbn10 = book_form.cleaned_data['isbn10']
                updated_book.isbn13 = book_form.cleaned_data['isbn13']
                updated_book.copyRightDate = book_form.cleaned_data['copyright_date']
                updated_book.edition = book_form.cleaned_data['edition']
                updated_book.numberOfPages = book_form.cleaned_data['num_pages']
                updated_book.type = book_form.cleaned_data['book_type']
                author = Author()
                author.author_id = int(book_form.cleaned_data['authors'])
                updated_book.author = author
                publisher = Publisher()
                publisher.publisher_id = int(book_form.cleaned_data['publishers'])
                updated_book.publisher = publisher
                genre = Genre()
                genre.genre_id = int(book_form.cleaned_data['genres'])
                updated_book.genre = genre                

                self.book_dao.update(updated_book)

                context['notification'] = "Book updated successfully!"
              
            else:
                context['notification'] = "Not a valid submission."

        if 'add-image' in request.POST:
            image_form = BookImageForm(request.POST, request.FILES)
            
            if image_form.is_valid():
                image_file = request.FILES['image']
                fs = FileSystemStorage()
                filename = fs.save(image_file.name, image_file)
                uploaded_file_url = fs.url(filename)

                image = Image()
                image.image_url = uploaded_file_url
                image.caption = ''
                image.book_id = book_id

                self.image_dao.create(image)

                context['notification'] = filename
            else:
                context['notification'] = "Not a valid submission."

        return render(request, self.template_name, context)


class CusBookView(TemplateView):
    template_name = 'Store/customer/books/books.html'
    book_dao = BookDao()
    
    def get(self, request):
        books = self.book_dao.get_all()

        context = {            
            'books': books
        }

        return render(request, self.template_name, context)


class CusBookDetailView(TemplateView):
    template_name = 'Store/customer/books/details.html'
    book_dao = BookDao()
    cart_dao = CartDao()
    image_dao = ImageDao()
    inventory_dao = InventoryDao()

    def get(self, request, book_id):
        book = self.book_dao.get_byid(book_id)
        images = self.image_dao.get_byid(book_id)
        inventory  = self.inventory_dao.get_byid(book_id)
        max_quantity = self.inventory_dao.get_byid(book_id).quantity_on_hand        
        cart_form = CartForm(max_quantity)

        context = {
            'book': book, 
            'images': images,
            'inventory': inventory,
            'cart_form': cart_form   
        }

        return render(request, self.template_name, context)

    def post(self, request, book_id):
        book = self.book_dao.get_byid(book_id)
        images = self.image_dao.get_byid(book_id)

        context = {
            'book': book,
            'images': images        
        }

        cart = Cart()
        cart.book.book_id = book_id
        cart.user_id = request.session['user_id']
        cart_form = CartForm(request.POST)        
        if cart_form.is_valid():
            cart.quantity_ordered = cart_form.cleaned_data['quantity_ordered']
            self.cart_dao.create(cart)

        return render(request, self.template_name, context)