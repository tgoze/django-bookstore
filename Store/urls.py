from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('', views.index, name='index'),
    path('admin/books', AdminBookView.as_view()),
    path('admin/books/details/<int:bookID>/', AdminBookDetailView.as_view())
]