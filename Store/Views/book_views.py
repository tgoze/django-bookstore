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
from Store.Model.inventory import Inventory
from Store.Model.inventory_dao import InventoryDao
from Store.Model.image import Image
from Store.Model.image_dao import ImageDao
from Store.Model.cart import Cart
from Store.Model.cart_dao import CartDao
from Store.forms import BookForm, BookImageForm, AuthorForm, PublisherForm, GenreForm, CartForm

from django.views.decorators.cache import never_cache

from django.conf import settings
from django.core.files.storage import FileSystemStorage


class AdminBookView(TemplateView):
    template_name = 'Store/admin/books/books.html'
    book_dao = BookDao()
    publisher_dao = PublisherDao()
    genre_dao = GenreDao()
    author_dao = AuthorDao()
    
    authors = []
    publishers = []
    genres = []

    # This gets the choices for the author, publisher, and genre dropdowns
    def get_dropdown_data(self):
        self.authors = []
        self.publishers = []
        self.genres = []
        self.authors.append(("default", {'label': "Choose an author", 'disabled': True}))
        for author in self.author_dao.get_all():
            author_val = (str(author.author_id), str(author.last_name) + ", " + str(author.first_name))
            self.authors.append(author_val)        
        self.publishers.append(("default", {'label': "Choose a publisher", 'disabled': True}))
        for publisher in self.publisher_dao.get_all():
            publisher_val = (str(publisher.publisher_id), str(publisher.company_name))
            self.publishers.append(publisher_val)        
        self.genres.append(("default", {'label': "Choose a genre", 'disabled': True}))
        for genre in self.genre_dao.get_all():
            genre_val = (str(genre.genre_id), str(genre.genre))
            self.genres.append(genre_val)
        
    @never_cache
    def get(self, request):
        context = {}
        if 'user_id' in request.session:
            if request.session['user_is_staff'] == 1:
                self.get_dropdown_data()            
                # Create forms for Django to handle
                book_form = BookForm(author_choices=self.authors, publisher_choices=self.publishers, genre_choices=self.genres)
                publisher_form = PublisherForm()
                author_form = AuthorForm()
                genre_form = GenreForm()
                books = self.book_dao.get_all()

                context = {            
                    'books': books,
                    'book_form': book_form,
                    'publisher_form': publisher_form,
                    'author_form': author_form,
                    'genre_form': genre_form,
                    'num_books': len(books)
                }

                context['user_id'] = request.session['user_id'],
                context['username'] = request.session['username']

                return render(request, self.template_name, context)
            else:
                return redirect(reverse('home'))    
        else:
            return redirect(reverse('login'))        
    
    @never_cache
    def post(self, request):
        context = {}    
        self.get_dropdown_data()
        # Handle POST requests
        if 'create-book' in request.POST:
            sub_book_form = BookForm(request.POST, author_choices=self.authors, publisher_choices=self.publishers, genre_choices=self.genres)
            book = Book()
            if sub_book_form.is_valid():               
                book.title = sub_book_form.cleaned_data['title']
                book.isbn10 = sub_book_form.cleaned_data['isbn10']
                book.isbn13 = sub_book_form.cleaned_data['isbn13']
                book.copyRightDate = sub_book_form.cleaned_data['copyright_date']
                book.edition = sub_book_form.cleaned_data['edition']
                book.numberOfPages = sub_book_form.cleaned_data['num_pages']
                book.type = sub_book_form.cleaned_data['book_type']
                author = Author()
                author.author_id = int(sub_book_form.cleaned_data['authors'])
                book.author = author
                publisher = Publisher()
                publisher.publisher_id = int(sub_book_form.cleaned_data['publishers'])
                book.publisher = publisher
                genre = Genre()
                genre.genre_id = int(sub_book_form.cleaned_data['genres'])
                book.genre = genre                
                book.inventory.quantity_on_hand = sub_book_form.cleaned_data['quantity_on_hand']
                book.inventory.cost = sub_book_form.cleaned_data['cost']
                book.inventory.retail_price = sub_book_form.cleaned_data['retail_price']

                self.book_dao.create(book)

                context['notification'] = "Book saved successfully!"
              
            else:
                context['notification'] = "Not a valid submission."                                    
        
        elif 'create-publisher' in request.POST:
            sub_publisher_form = PublisherForm(request.POST)
            publisher = Publisher()
            if sub_publisher_form.is_valid():
                publisher.company_name = sub_publisher_form.cleaned_data['company_name']
                publisher.city = sub_publisher_form.cleaned_data['city']
                publisher.state_code = sub_publisher_form.cleaned_data['state_code']
                publisher.zip_code = sub_publisher_form.cleaned_data['zip_code']
                publisher.phone_number = sub_publisher_form.cleaned_data['phone_number']
                publisher.contact_name = sub_publisher_form.cleaned_data['contact_name']
                self.publisher_dao.create(publisher)
                
                context['notification'] = "Publisher saved successfully!"
            else:
                context['notification'] = "Not a valid submission."         
        
        elif 'create-author' in request.POST:
            sub_author_form = AuthorForm(request.POST)
            author = Author()            
            if sub_author_form.is_valid():
                author.first_name = sub_author_form.cleaned_data['first_name']
                author.last_name = sub_author_form.cleaned_data['last_name']

                self.author_dao.create(author) 
                
                context['notification'] = "Author saved successfully!"
            else:
                context['notification'] = "Not a valid submission."

        elif 'create-genre' in request.POST:
            sub_genre_form = GenreForm(request.POST)
            genre = Genre()
            if sub_genre_form.is_valid():
                genre.genre = sub_genre_form.cleaned_data['genre']                

                self.genre_dao.create(genre) 
                
                context['notification'] = "Genre saved successfully!"
            else:
                context['notification'] = "Not a valid submission."        

        # Pass data so the page is usable after a post  
        self.get_dropdown_data()
        book_form = BookForm(author_choices=self.authors, publisher_choices=self.publishers, genre_choices=self.genres)               
        publisher_form = PublisherForm()    
        author_form = AuthorForm()
        genre_form = GenreForm()        

        context['book_form'] = book_form
        context['publisher_form'] = publisher_form
        context['author_form'] = author_form
        context['genre_form'] = genre_form
        books = self.book_dao.get_all()
        context['books'] = books
        context['num_books'] = len(books)

        return render(request, self.template_name, context)


class AdminBookDetailView(TemplateView):
    template_name = 'Store/admin/books/details.html'    
    book_dao = BookDao()
    image_dao = ImageDao()
    inventory_dao = InventoryDao()

    publisher_dao = PublisherDao()
    genre_dao = GenreDao()
    author_dao = AuthorDao()

    # This gets the choices for the author, publisher, and genre dropdowns
    authors = []
    authors.append(("default", {'label': "Choose an author", 'disabled': True}))
    for author in author_dao.get_all():
        author_val = (str(author.author_id), str(author.last_name) + ", " + str(author.first_name))
        authors.append(author_val)
    publishers = []
    publishers.append(("default", {'label': "Choose a publisher", 'disabled': True}))
    for publisher in publisher_dao.get_all():
        publisher_val = (str(publisher.publisher_id), str(publisher.company_name))
        publishers.append(publisher_val)
    genres = []
    genres.append(("default", {'label': "Choose a genre", 'disabled': True}))
    for genre in genre_dao.get_all():
        genre_val = (str(genre.genre_id), str(genre.genre))
        genres.append(genre_val)
    
    @never_cache
    def get(self, request, book_id):
        book = self.book_dao.get_byid(book_id)
        images = self.image_dao.get_byid(book_id)

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
        book_form = BookForm(initial_data, author_choices=self.authors, publisher_choices=self.publishers, genre_choices=self.genres)
        image_form = BookImageForm()        

        context = {
            'book': book,
            'images': images,
            'book_form': book_form,
            'image_form': image_form
        }

        return render(request, self.template_name, context)

    def post(self, request, book_id):
        book_form = BookForm(request.POST, author_choices=self.authors, publisher_choices=self.publishers, genre_choices=self.genres)
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

        elif 'delete-book' in request.POST:
            book_id = int(request.POST.get('delete-book'))
            self.book_dao.delete(book_id)

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
    
    @never_cache
    def get(self, request):
        if 'user_id' in request.session:
            books = self.book_dao.get_all()
            username = request.session['username'] 
            context = {            
                'user_id': request.session['user_id'],
                'books': books
            }
            context['username'] = request.session['username']
            return render(request, self.template_name, context)
        else:
            return redirect(reverse('login'))


class CusBookDetailView(TemplateView):
    template_name = 'Store/customer/books/details.html'
    book_dao = BookDao()
    cart_dao = CartDao()
    image_dao = ImageDao()
    inventory_dao = InventoryDao()

    @never_cache
    def get(self, request, book_id):
        if 'user_id' in request.session:
            book = self.book_dao.get_byid(book_id)
            images = self.image_dao.get_byid(book_id)
            max_quantity = self.inventory_dao.get_byid(book_id).quantity_on_hand
            cart_form = CartForm(max_quantity=max_quantity)

            context = {
                'user_id': request.session['user_id'],
                'book': book, 
                'images': images,
                'cart_form': cart_form   
            }

            return render(request, self.template_name, context)
        else:
            return redirect(reverse('login'))

    def post(self, request, book_id):
        max_quantity = self.inventory_dao.get_byid(book_id).quantity_on_hand
        cart_item = Cart()
        cart_item.book.book_id = book_id
        cart_item.user_id = request.session['user_id']
        cart_form = CartForm(request.POST, max_quantity=max_quantity)        
        if cart_form.is_valid():
            cart_item.quantity_ordered = cart_form.cleaned_data['quantity_ordered']
            self.cart_dao.create(cart_item)

        return redirect(reverse('cart'))