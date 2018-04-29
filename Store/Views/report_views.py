from django.shortcuts import render, redirect, reverse
from django.views.generic import TemplateView
from Store.Model.book import Book
from Store.Model.book_dao import BookDao
from Store.Model.author import Author
from Store.Model.author_dao import AuthorDao
from Store.Model.publisher import Publisher
from Store.Model.publisher_dao import PublisherDao
from Store.Model.genre import Genre
from Store.Model.genre_dao import GenreDao
from Store.Model.customer_info_dao import CustomerInfoDAO
from Store.Model.user import User
from Store.Model.user_dao import UserDao
from Store.Model.customer_info import CustomerInfo
from Store.Model.customer_address_dao import CustomerAddressDao
from Store.Model.customer_address import CustomerAddress
from Store.Model.payment_info import PaymentInfo
from Store.Model.payment_info_dao import PaymentInfoDao
from Store.Model.inventory import Inventory
from Store.Model.inventory_dao import InventoryDao
from Store.Model.retail_order import RetailOrder
from Store.Model.retail_order_dao import RetailOrderDao
from Store.Model.book_order import BookOrder
from Store.Model.book_order_dao import BookOrderDao
from Store.Model.report_dao import ReportDao
from django.conf import settings
from django.contrib.auth.hashers import check_password, BCryptPasswordHasher,make_password
from Store.forms import *
from bcrypt import *
from django.views.decorators.cache import never_cache

class AdminReportIndex(TemplateView):
    template_name = 'Store/admin/reports/reports.html'
    rdao = ReportDao()
    
    @never_cache
    def get(self,request):
       
        context = {
            'jan_revenue': self.rdao.getJanuaryRevenue(),
            'feb_revenue':self.rdao.getFebruaryRevenue(),
            'mar_revenue':self.rdao.getMarchRevenue(),
            'apr_revenue':self.rdao.getAprilRevenue(),
            'total': self.rdao.getTotalRevenue(),
            'avg': self.rdao.getAVGTransactionAmount(),
            'num': self.rdao.getTotalNumberOfOrders()
        }
        user_id =  request.session['user_id'] 
        username = request.session['username'] 
        context['user_id'] = request.session['user_id']
        context['username'] = request.session['username']
        return render(request,self.template_name, context) 

class AdminJanReport(TemplateView):
    template_name = 'Store/admin/reports/jan.html'
    rdao = ReportDao()
    
    @never_cache
    def get(self,request):
        orders = self.rdao.getJanuaryOrders()
        jan_revenue = self.rdao.getJanuaryRevenue()
        num = len(orders)
        context = {
            'orders': orders,
            'jan_revenue': jan_revenue,
            'num': num
        }
        user_id =  request.session['user_id'] 
        username = request.session['username'] 
        context['user_id'] = request.session['user_id']
        context['username'] = request.session['username']
        return render(request, self.template_name, context)

class AdminFebReport(TemplateView):
    template_name = 'Store/admin/reports/feb.html'
    rdao = ReportDao()
    
    @never_cache
    def get(self,request):
        orders = self.rdao.getFebruaryOrders()
        feb_revenue = self.rdao.getFebruaryRevenue()
        num = len(orders)
        context = {
            'orders': orders,
            'feb_revenue': feb_revenue,
            'num': num
        }
        user_id =  request.session['user_id'] 
        username = request.session['username'] 
        context['user_id'] = request.session['user_id']
        context['username'] = request.session['username']
        return render(request, self.template_name, context)

class AdminMarchReport(TemplateView):
    template_name = 'Store/admin/reports/mar.html'
    rdao = ReportDao()
    
    @never_cache
    def get(self,request):
        orders = self.rdao.getMarchOrders()
        mar_revenue = self.rdao.getMarchRevenue()
        num = len(orders)
        context = {
            'orders': orders,
            'mar_revenue': mar_revenue,
            'num': num
        }
        user_id =  request.session['user_id'] 
        username = request.session['username'] 
        context['user_id'] = request.session['user_id']
        context['username'] = request.session['username']
        return render(request, self.template_name, context)

class AdminAprilReport(TemplateView):
    template_name = 'Store/admin/reports/apr.html'
    rdao = ReportDao()
    
    @never_cache
    def get(self,request):
        orders = self.rdao.getAprilOrders()
        apr_revenue = self.rdao.getAprilRevenue()
        num = len(orders)
        context = {
            'orders': orders,
            'apr_revenue': apr_revenue,
            'num': num
        }
        user_id =  request.session['user_id'] 
        username = request.session['username'] 
        context['user_id'] = request.session['user_id']
        context['username'] = request.session['username']
        return render(request, self.template_name, context)