from django.urls import path
from Store.Views.home_views import *
from Store.Views.book_views import *
from Store.Views.customer_views import *
from Store.Views.order_views import *
from Store.Views.admin_views import *
from Store.Views.publisher_views import *
from Store.Views.genre_views import * 
from Store.Views.author_views import *
from Store.Views.admin_order_views import *
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('login', LoginView.as_view(), name='login'),
    path('admin/index', AdminIndexView.as_view(), name='adminindex'),
    path('admin/books', AdminBookView.as_view(), name='adminbookindex'),
    path('admin/books/details/<int:book_id>/', AdminBookDetailView.as_view()),
    path('admin/customers', AdminCustomerView.as_view(), name='admincustomerindex'),
    path('admin/customers/details/<int:customer_id>/', AdminCustomerDetailView.as_view()),
    path('admin/genres', AdminGenreIndexView.as_view(), name='admingenreindex'),
    path('admin/publishers', AdminPublisherIndexView.as_view(), name='adminpublisherindex'),
    path('admin/publishers/details/<int:publisher_id>/', AdminPublisherDetailView.as_view(), name='adminpublisherdetail'),
    path('admin/inventory', AdminInventoryView.as_view(), name='admininventoryindex'),
    path('admin/genres/details/<int:genre_id>/', AdminGenreDetailsView.as_view(), name='admingenredetail'),
<<<<<<< HEAD
    
    path('customer/books', CusBookView.as_view(), name="customer_books"),
=======
    path('admin/authors', AdminAuthorView.as_view(), name='adminauthorindex'),
    path('admin/authors/details/<int:author_id>/', AdminAuthorDetailView.as_view(), name='adminauthordetail'),
    path('admin/orders', AdminOrderView.as_view(), name='adminorderindex'),
    path('admin/orders/details/<int:order_id>/', AdminOrderDetailView.as_view(), name='adminorderdetail'),

    path('customer/books', CusBookView.as_view()),
>>>>>>> kara_line
    path('customer/books/details/<int:book_id>/', CusBookDetailView.as_view(), name="customer_book"),   
    path('customer/cart', CartView.as_view(), name="cart"),
    path('customer/shippay', ShipPayView.as_view(), name="ship_pay"),
    path('customer/checkout', CheckOutView.as_view(), name="checkout"),  
    path('customer/invoice', InvoiceView.as_view(), name="invoice"),    
    path('customer/customeraccount', CustomerAccountView.as_view(), name='customeraccount'),
<<<<<<< HEAD
    path('customer/index', CustomerIndexView.as_view(), name='customer_index'),
    path('customer/caddressaccount/<int:address_id>',CAddressAccountView.as_view()),
    path('customer/ccard/<int:card_id>/', CustomerCardView.as_view()),
    path('customer/addcard', CustomerAddCardView.as_view())
=======
    path('customer/index', CustomerIndexView.as_view(), name='customerindex'),
    path('customer/caddressaccount/<int:address_id>',CAddressAccountView.as_view(), name='customeraddress'),
    path('customer/ccard/<int:card_id>/', CustomerCardView.as_view(), name='customercard' ),
    path('customer/addcard', CustomerAddCardView.as_view(), name='customeraddcard'),
    path('customer/corder/<int:order_id>/', CustomerOrderView.as_view(), name='customerorder')
>>>>>>> kara_line
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
