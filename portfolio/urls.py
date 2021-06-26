from django.urls import path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns
from .views import (
    CustomerList, 
    CustomerUpdate, 
    CustomerDelete,
    CustomerCreate, 
    HomeView, 
    StockList, 
    StockCreate,
    StockUpdate, 
    StockDelete,
    InvestmentList,
    InvestmentCreate,
    InvestmentUpdate,
    InvestmentDelete,
    PassiveList,
    PassiveCreate,
    PassiveUpdate,
    PassiveDelete,
    CustomerListAPI,
    SignUpView,
    )

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    # CUSTOMER URLS
    path('customer_list', CustomerList.as_view(), name='customer_list'),
    path('add_customer', CustomerCreate.as_view(), name='add_customer'),
    path('customer/<int:pk>/edit', CustomerUpdate.as_view(), name='customer_update'),
    path('customer/<int:pk>/delete', CustomerDelete.as_view(), name='customer_delete'),
    # STOCK URLS
    path('stock_list', StockList.as_view(), name='stock_list'),
    path('add_stock', StockCreate.as_view(), name='add_stock'),
    path('stock/<int:pk>/edit', StockUpdate.as_view(), name='edit_stock'),
    path('stock/<int:pk>/delete', StockDelete.as_view(), name='delete_stock'),
    # INVESTMENT URLS
    path('invesment_list', InvestmentList.as_view(), name='investment_list'),
    path('add_investment', InvestmentCreate.as_view(), name='add_investment'),
    path('investment/<int:pk>/edit', InvestmentUpdate.as_view(), name='edit_investment'),
    path('investment/<int:pk>/delete', InvestmentDelete.as_view(), name='delete_investment'),
     # PASSIVE URLS
    path('passive_list', PassiveList.as_view(), name='passive_list'),
    path('add_passive', PassiveCreate.as_view(), name='add_passive'),
    path('passive/<int:pk>/edit', PassiveUpdate.as_view(), name='edit_passive'),
    path('passive/<int:pk>/delete', PassiveDelete.as_view(), name='delete_passive'),
    # PORTFOLIO URLS
    path('customer/<int:pk>/portfolio', views.portfolio, name='portfolio'),
    # SERIALIZER 
    path('customers_json/', views.CustomerListAPI.as_view()),
    # PDF
    path('pdf/<int:pk>/pdf_portfolio', views.pdf_view, name='pdf_portfolio'),
    # PROFILE URLS
    path('signup/', SignUpView.as_view(), name='signup' ),
]

urlpatterns = format_suffix_patterns(urlpatterns)