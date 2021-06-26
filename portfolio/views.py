from django.shortcuts import get_object_or_404, render
from .models import Customer, Investment, Stock, Passive
from django.views.generic import ListView, UpdateView, DeleteView, TemplateView, CreateView, View
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import CustomerSerializer
from django.http import HttpResponse
from .utils import render_to_pdf

class HomeView(TemplateView):
    template_name = "portfolio/home.html"

# CUSTOMER VIEWS
class CustomerList(LoginRequiredMixin, ListView):
    model = Customer

class CustomerCreate(LoginRequiredMixin, CreateView):
    model = Customer
    template_name = 'portfolio/customer_add.html'
    fields = ['cust_number','name', 'address', 'city', 'state', 'zipcode', 'email', 'cell_phone']
    success_url = reverse_lazy('customer_list')

class CustomerUpdate(LoginRequiredMixin, UpdateView):
    model = Customer
    fields = ['name', 'address', 'city', 'state', 'zipcode', 'email', 'cell_phone']
    success_url = reverse_lazy('customer_list')

class CustomerDelete(LoginRequiredMixin, DeleteView):
    model = Customer
    success_url = reverse_lazy('customer_list')

# STOCK VIEWS
class StockList(LoginRequiredMixin, ListView):
    model = Stock

class StockCreate(LoginRequiredMixin, CreateView):
    model = Stock
    template_name = 'portfolio/stock_add.html'
    fields = ['customer','symbol','name','shares','purchase_price']
    success_url = reverse_lazy('stock_list')

class StockUpdate(LoginRequiredMixin, UpdateView):
    model = Stock
    fields = ['customer','symbol','name','shares','purchase_price']
    success_url = reverse_lazy('stock_list')

class StockDelete(LoginRequiredMixin, DeleteView):
    model = Stock
    success_url = reverse_lazy('stock_list')

# INVESTMENT VIEWS
class InvestmentList(LoginRequiredMixin, ListView):
    model = Investment

class InvestmentCreate(LoginRequiredMixin, CreateView):
    model = Investment
    template_name = 'portfolio/investment_add.html'
    fields = ['customer','category','description','acquired_value','acquired_date','recent_value']
    success_url = reverse_lazy('investment_list')

class InvestmentUpdate(LoginRequiredMixin, UpdateView):
    model = Investment
    fields = ['customer','category','description','acquired_value','acquired_date','recent_value']
    success_url = reverse_lazy('investment_list')

class InvestmentDelete(LoginRequiredMixin, DeleteView):
    model = Investment
    success_url = reverse_lazy('investment_list')

# PASSIVE VIEWS
class PassiveList(LoginRequiredMixin, ListView):
    model = Passive

class PassiveCreate(LoginRequiredMixin, CreateView):
    model = Passive
    template_name = 'portfolio/passive_add.html'
    fields = ['customer','category','description','acquired_value','acquired_date','monthly_cost','monthly_profit']
    success_url = reverse_lazy('passive_list')

class PassiveUpdate(LoginRequiredMixin, UpdateView):
    model = Passive
    fields = ['customer','category','description','acquired_value','acquired_date','monthly_cost','monthly_profit']
    success_url = reverse_lazy('passive_list')

class PassiveDelete(LoginRequiredMixin, DeleteView):
    model = Passive
    success_url = reverse_lazy('passive_list')

@login_required
def portfolio(request,pk):
    customer = get_object_or_404(Customer, pk=pk)
    customers = Customer.objects.filter(created_date__lte=timezone.now())
    investments =Investment.objects.filter(customer=pk)
    stocks = Stock.objects.filter(customer=pk)
    passives = Passive.objects.filter(customer=pk)
    sum_recent_value = Investment.objects.filter(customer=pk).aggregate(Sum('recent_value'))
    sum_acquired_value = Investment.objects.filter(customer=pk).aggregate(Sum('acquired_value'))
    investment_recent_value = sum_recent_value['recent_value__sum']
    investment_acquired_value = sum_acquired_value['acquired_value__sum']
    #overall_investment_results = sum_recent_value-sum_acquired_value
    # Initialize the value of the stocks
    sum_current_stocks_value = 0
    sum_of_initial_stock_value = 0
    
    # Loop through each stock and add the value to the total
    for stock in stocks:
        sum_current_stocks_value += stock.current_stock_value()
        sum_of_initial_stock_value += stock.initial_stock_value()

    return render(request, 'portfolio/portfolio.html', {'customers': customers,
                                                       'investments': investments,
                                                       'stocks': stocks,
                                                       'customer': customer,
                                                       'passives': passives,
                                                       'sum_acquired_value': investment_acquired_value,
                                                       'sum_recent_value': investment_recent_value,
                                                        'sum_current_stocks_value': sum_current_stocks_value,
                                                        'sum_of_initial_stock_value': sum_of_initial_stock_value,})

class CustomerListAPI(APIView):
    def get(self,request):
        customers_json = Customer.objects.all()
        serializer = CustomerSerializer(customers_json,many=True)
        return Response(serializer.data)

# PDF GENERATION
""" class GeneratePdf(View):
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['customer'] = Customer.objects.all()
        return context

    def get(self, request, *args, **kwargs):
        pdf = render_to_pdf('portfolio/pdf_portfolio.html', )
        return HttpResponse(pdf, content_type='application/pdf') """

def pdf_view(request, pk, *args, **kwargs):
        customer = get_object_or_404(Customer, pk=pk)
        customers = Customer.objects.filter(created_date__lte=timezone.now())
        investments =Investment.objects.filter(customer=pk)
        stocks = Stock.objects.filter(customer=pk)
        passives = Passive.objects.filter(customer=pk)
        sum_recent_value = Investment.objects.filter(customer=pk).aggregate(Sum('recent_value'))
        sum_acquired_value = Investment.objects.filter(customer=pk).aggregate(Sum('acquired_value'))
        investment_recent_value = sum_recent_value['recent_value__sum']
        investment_acquired_value = sum_acquired_value['acquired_value__sum']
        #overall_investment_results = sum_recent_value-sum_acquired_value
        # Initialize the value of the stocks
        sum_current_stocks_value = 0
        sum_of_initial_stock_value = 0

        #Loop through each stock and add the value to the total
        for stock in stocks:
            sum_current_stocks_value += stock.current_stock_value()
            sum_of_initial_stock_value += stock.initial_stock_value()

        pdf = render_to_pdf('portfolio/pdf_portfolio.html', {'customers': customers,
                                                       'investments': investments,
                                                       'stocks': stocks,
                                                       'passives': passives,
                                                       'customer': customer,
                                                       'sum_acquired_value': investment_acquired_value,
                                                       'sum_recent_value': investment_recent_value,
                                                        'sum_current_stocks_value': sum_current_stocks_value,
                                                        'sum_of_initial_stock_value': sum_of_initial_stock_value,})
        return HttpResponse(pdf, content_type='application/pdf')

# accounts/views.py
from .forms import CustomUserCreationForm

class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'