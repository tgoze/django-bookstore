from django.urls import path
from Store.Views.home_views import *
from Store.Views.book_views import *
from Store.Views.user_views import *
from Store.Views.order_views import *

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('login', LoginView.as_view(), name='login'),
    path('admin/index', AdminIndexView.as_view()),
    path('admin/books', AdminBookView.as_view()),
    path('admin/books/details/<int:book_id>/', AdminBookDetailView.as_view()),
    path('admin/customers', AdminCustomerView.as_view()),
    path('admin/customers/details/<int:customer_id>/', AdminCustomerDetailView.as_view()),
    path('admin/inventory', AdminInventoryView.as_view()),
    path('customer/books', CusBookView.as_view()),
    path('customer/cart', CartView.as_view(), name="cart"),
    path('customer/shippay', ShipPayView.as_view(), name="ship_pay"),
    path('customer/checkout', CheckOutView.as_view(), name="checkout"),
    path('customer/books/details/<int:book_id>/', CusBookDetailView.as_view(), name="customer_book"),   
    path('customer/customeraccount', CustomerAccountView.as_view(), name='customeraccount'),
    path('customer/index', CustomerIndexView.as_view()),
    path('customer/caddressaccount/<int:address_id>',CAddressAccountView.as_view()),
    path('customer/addcard', CustomerAddCardView.as_view())
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
