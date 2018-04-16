from django.shortcuts import render
from django.views.generic import TemplateView
from Store.Model.book import Book
from Store.Model.book_dao import BookDao
from Store.Model.author import Author
from Store.Model.publisher import Publisher
from Store.Model.genre import Genre
from Store.Model.customer_info_dao import CustomerInfoDAO
from Store.Model.user import User
from Store.Model.user_dao import UserDao
from Store.Model.customer_address import CustomerAddress
from django.conf import settings
from django.contrib.auth.hashers import check_password, BCryptPasswordHasher,make_password
from .forms import *
from bcrypt import*

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

        return render(request,self.template_name, context)
class AdminTestView(TemplateView):
    u = User()
    template_name = 'Store/customer/admin.html'
    def get(self,request):
        user_id = request.session['user_id']
        context = {
            'user_id': user_id
        }
        return render(request,self.template_name, context)
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
    template_name = 'Store/customer/login.html'
    def get(self,request):  
        form = LoginForm()  
        form1 = RegisterUserForm()
        context = {
            'form': form,
           # 'form1': form1
        }

        return render(request, self.template_name, context)
    def post(self,request):
        #settings.configure(DEBUG=True)
        user = User()
        udao = UserDao()

        form = LoginForm(request.POST)
        form1 = RegisterUserForm(request.POST)
        if 'login' in request.POST:
            if form.is_valid():
                user.username = form.cleaned_data['username']
                user.password = form.cleaned_data['password']
                
                if (check_password(user.password,udao.get_byusername(user.username).password) == True):
                    
                    user.id = self.udao.get_byusername(user.username).id
                    user = self.udao.get_byid(user.id)
                    
                request.session['user_id'] = user.id
                
            return render(request,self.template_name, context=None)

        if 'create-user' in request.POST:
            if form1.is_valid():
                    user.first_name = form1.cleaned_data['first_name']
                    user.last_name = form1.cleaned_data['last_name']
                    user.email = form1.cleaned_data['last_name']
                    user.username = form1.cleaned_data['username']
                    x = form1.cleaned_data['password']
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
                    'text':'try again'
                }

            return render(request,self.template_name, context)

