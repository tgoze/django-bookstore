from django.urls import path
from . import views
from Store.Views.book_views import *
from Store.Views.user_views import *
# from .views import AdminCustomerView, LoginView, TestView

urlpatterns = [
    path('', views.index, name='index'),
    path('admin/books', AdminBookView.as_view()),
    path('admin/books/details/<int:bookID>/', AdminBookDetailView.as_view()),
    path('admin/customers', AdminCustomerView.as_view()),
    #path('admin/customers/details/<int:customer_id>/', admin_customer_details(), name='admin_customer_details'),
    path('customer/',(LoginView.as_view())),
    path('customer/test/', TestView.as_view()),
    path('customer/',LoginView.as_view()),
    path('customer/customeraccount/<int:user_id>/',CustomerAccountView.as_view())

]