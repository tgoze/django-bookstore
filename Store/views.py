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
from Store.Model.customer_info_dao import CustomerInfoDAO
from Store.Model.user import User
from Store.Model.user_dao import UserDao
from Store.Model.customer_address import CustomerAddress
from django.conf import settings
from django.contrib.auth.hashers import check_password, BCryptPasswordHasher,make_password
from .forms import *
from bcrypt import *

def index(request): 
    return render(request, 'Store/index.html')


class TestView(TemplateView):
    u = User()
    template_name = 'Store/customer/test.html'
    def get(self,request):
        user_id = request.session['user_id']
        context = {
            'user_id': user_id
        }

        return render(request,self.template_name,context)


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
                book.image_id = 1

                self.book_dao.create(book)

                context = {
                    'notification': "Book saved successfully!",
                    'books': books,
                    'book_form': book_form
                }
            else:
                context = {
                    'notification': "Not a valid submission."
                }

            return render(request, self.template_name, context)

        elif 'delete-book' in request.POST:
            book_id = int(request.POST.get('delete-book'))
            self.book_dao.delete(book_id)

            context = {                
                'books': books,
                'book_form': book_form
            }

            return render(request, self.template_name, context)
        
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
            
            return render(request, self.template_name, context)
        
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
            
            return render(request, self.template_name, context)

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
    
    def get(self, request, bookID):
        book = self.book_dao.get_byid(bookID)
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
        form = BookForm(initial_data)        

        context = {
            'book': book,
            'form': form
        }

        return render(request, 'Store/admin/books/details.html', context)

    def post(self, request, bookID):
        book = self.book_dao.get_byid(bookID)
    
        context = {
            'book': book
        }

        return render(request, 'Store/admin/books/details.html', context)


class AdminCustomerView(TemplateView):
    template_name = 'Store/admin/customers/customers.html'
    
    def get(self,request):
        cdao = CustomerInfoDAO()

        customers = cdao.get_all()
        context = {
            'customers': customers
        }
        return render(request, self.template_name, context)


def admin_customer_details(request,customer_id):
    cdao = CustomerInfoDAO()

    customer = cdao.get_byid(customer_id)
    customer_address = cdao.get_addressbyid(customer_id)
    context = {
        'customer': customer,
        'caddress': customer_address
    }
    return render(request,'Store/admin/customers/details.html', context)


class LoginView(TemplateView):
    user = User()
    udao = UserDao()
    login_template = 'Store/customer/login.html'
    loggedin_template = 'Store/customer/test.html'
    user.username = 'not logged in'

    def get(self, request):  
        loginform = LoginForm()  
        registerform = RegisterUserForm()
        context = {
            'loginform': loginform,
            'registerform': registerform           
        }

        return render(request, self.login_template, context)

    def post(self, request):
        #settings.configure(DEBUG=True)
        user = User()
        udao = UserDao()

        login_form = LoginForm(request.POST)
        register_form = RegisterUserForm(request.POST)

        if 'login-user' in request.POST:
            if login_form.is_valid():
                user.username = login_form.cleaned_data['username']
                user.password = login_form.cleaned_data['password']
                user.id = udao.get_byusername(user.username).id
                if check_password(user.password,udao.get_byusername(user.username).password):
                    request.session['user_id'] = user.id
                    request.session['username'] = user.username
                    context = {
                        'text': 'Yay password',
                        'user_id': request.session['user_id'],
                        'username': request.session['username']
                    }                    
                else:
                    context = {
                        'text': 'Bad password bro',
                        'user_id': None
                    }    
            else:
                context = {
                    'text': 'try again',
                    'user_id': None
                }

            return render(request, self.loggedin_template, context)

        if 'create-user' in request.POST:        
            if register_form.is_valid():
                user.first_name = register_form.cleaned_data['first_name']
                user.last_name = register_form.cleaned_data['last_name']
                user.email = register_form.cleaned_data['last_name']
                user.username = register_form.cleaned_data['username']
                x = register_form.cleaned_data['password']
                user.is_superuser = 0
                user.is_active = 1
                user.is_staff = 0
                user.password = make_password(x,salt=None,hasher='default')
                udao.create(user)
                context = {
                    'text': 'user saved???'            
                }
            else:
                context = {
                    'text': 'try again'                    
                }
                
            return render(request,self.login_template, context)

