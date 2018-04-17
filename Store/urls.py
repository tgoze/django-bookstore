from django.urls import path
from . import views
from Store.Views.home_views import *
from Store.Views.book_views import *
from Store.Views.user_views import *

urlpatterns = [
    path('', HomeView.as_view()),
    path('login', LoginView.as_view()),
    path('admin/books', AdminBookView.as_view()),
    path('admin/books/details/<int:bookID>/', AdminBookDetailView.as_view()),
    path('admin/customers', AdminCustomerView.as_view()),
    path('customer/customeraccount/<int:user_id>/', CustomerAccountView.as_view()),
    path('admin/customers/details/<int:customer_id>/', AdminCustomerDetailView.as_view())
    
]