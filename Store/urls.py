from django.urls import path
from . import views
from .views import AdminBookView, AdminCustomerView

urlpatterns = [
    path('', views.index, name='index'),
    path('admin/books', AdminBookView.as_view()),
    path('admin/books/details/<int:bookID>/', views.admin_book_details, name='admin_books_details'),
    path('admin/customers', AdminBookView.as_view())
]