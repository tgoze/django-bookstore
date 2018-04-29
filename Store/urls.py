from django.urls import path
from Store.Views.home_views import *
from Store.Views.book_views import *
from Store.Views.customer_views import *
from Store.Views.order_views import *
from Store.Views import order_views
from Store.Views.admin_views import *
from Store.Views.publisher_views import *
from Store.Views.genre_views import * 
from Store.Views.author_views import *
from Store.Views.admin_order_views import *
from Store.Views.report_views import *
from Store.Views.admin_book_views import *
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('login', LoginView.as_view(), name='login'),

    path('admin/index', AdminIndexView.as_view(), name='adminindex'),

    path('admin/books', AdminBookView.as_view(), name='adminbookindex'),
    path('admin/books/details/<int:book_id>/', AdminBookDetailView.as_view(), name='adminbookdetail'),
    path('admin/books/addbook', AdminAddBookView.as_view(), name='adminaddbook'),

    path('admin/customers', AdminCustomerView.as_view(), name='admincustomerindex'),
    path('admin/customers/details/<int:customer_id>/', AdminCustomerDetailView.as_view(), name='admincustomerdetail'),
    path('admin/customers/states', AdminCustomerByStateView.as_view(), name='admincustomerstates'),
    path('admin/customers/repeats', AdminCustomerRepeatView.as_view(), name='admincustomerrepeat'),

    path('admin/genres', AdminGenreIndexView.as_view(), name='admingenreindex'),
    path('admin/genres/details/<int:genre_id>/', AdminGenreDetailsView.as_view(), name='admingenredetail'),

    path('admin/publishers', AdminPublisherIndexView.as_view(), name='adminpublisherindex'),
    path('admin/publishers/details/<int:publisher_id>/', AdminPublisherDetailView.as_view(), name='adminpublisherdetail'),

    path('admin/inventory', AdminInventoryView.as_view(), name='admininventoryindex'),
    path('admin/authors', AdminAuthorView.as_view(), name='adminauthorindex'),
    path('admin/authors/details/<int:author_id>/', AdminAuthorDetailView.as_view(), name='adminauthordetail'),

    path('admin/orders', AdminOrderView.as_view(), name='adminorderindex'),
    path('admin/orders/details/<int:order_id>/', AdminOrderDetailView.as_view(), name='adminorderdetail'),

    path('admin/reports', AdminReportIndex.as_view(), name='adminreportindex'),
    path('admin/jan', AdminJanReport.as_view(), name='january'),
    path('admin/feb', AdminFebReport.as_view(), name='february'),
    path('admin/mar', AdminMarchReport.as_view(), name='march'),
    path('admin/apr', AdminAprilReport.as_view(), name='april'),
    
    path('customer/books', CusBookView.as_view(), name="customer_books"),
    path('customer/books/details/<int:book_id>/', CusBookDetailView.as_view(), name="customer_book"),   
    path('customer/cart', CartView.as_view(), name="cart"),
    path('customer/cart/ajax/update/', update_cart_view, name="cart_update"),
    path('customer/shippay', ShipPayView.as_view(), name="ship_pay"),
    path('customer/checkout', CheckOutView.as_view(), name="checkout"),  
    path('customer/invoice', InvoiceView.as_view(), name="invoice"),    
    path('customer/customeraccount', CustomerAccountView.as_view(), name='customeraccount'),
    path('customer/index', CustomerIndexView.as_view(), name='customer_index'),
    path('customer/caddressaccount/<int:address_id>',CAddressAccountView.as_view(), name='customeraddress'),
    path('customer/ccard/<int:card_id>/', CustomerCardView.as_view(), name='customercard' ),
    path('customer/addcard', CustomerAddCardView.as_view(), name='customeraddcard'),
    path('customer/corder/<int:order_id>/', CustomerOrderView.as_view(), name='customerorder')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
