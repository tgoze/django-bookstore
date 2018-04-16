from django.urls import path
<<<<<<< HEAD
from . import views
from .views import *
=======
# from . import views
from Store.Views.book_views import *
from Store.Views.user_views import *
# from .views import AdminCustomerView, LoginView, TestView
>>>>>>> origin/tgoze

urlpatterns = [
    path('', views.index, name='index'),
    path('admin/books', AdminBookView.as_view()),
    path('admin/books/details/<int:bookID>/', AdminBookDetailView.as_view()),
    path('admin/customers', AdminCustomerView.as_view()),
<<<<<<< HEAD
    path('admin/customers/details/<int:customer_id>/', views.admin_customer_details, name='admin_customer_detailss'),
    path('customer/test/', TestView.as_view()),
    path('customer/',LoginView.as_view()),
    path('customer/admin/', AdminTestView.as_view()),
=======
    path('admin/customers/details/<int:customer_id>/', views.admin_customer_details(), name='admin_customer_detailss'),
    path('customer/',(LoginView.as_view())),
    path('customer/test/', TestView.as_view()),
    path('customer/',LoginView.as_view())

>>>>>>> origin/tgoze
]