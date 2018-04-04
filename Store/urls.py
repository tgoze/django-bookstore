from django.urls import path
from . import views

# TODO make a freaking template bro
urlpatterns = [
    path('', views.index, name='index')
]