from django.urls import path
from . import views

# TODO make a freaking template bro
urlpatterns = [
    path('', views.index, name='index'),
    path('admin/books', views.admin_books, name='admin_books'),
    path('admin/books/details/<int:bookID>/', views.admin_book_details, name='admin_books')
]