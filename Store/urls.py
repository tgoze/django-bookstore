from django.urls import path
from . import views
from .views import AdminBookView, AdminCustomerView, LoginView

urlpatterns = [
    path('', views.index, name='index'),
    path('admin/books', AdminBookView.as_view()),
    path('admin/books/details/<int:bookID>/', views.admin_book_details, name='admin_books_details'),
    path('admin/customers', AdminCustomerView.as_view()),
    path('admin/customers/details/<int:customer_id>/', views.admin_customer_details, name='admin_customer_detailss'),
    path('customer/',LoginView.as_view())
   
]