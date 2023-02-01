from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages

from electro.filters import *
from electro.models import *
from django.contrib.auth import authenticate, login, logout


@login_required(login_url='login')
def index(request):
    t_sale_invoice = SaleInvoice.objects.select_related().count()
    t_sale = SaleItem.objects.values_list().aggregate(Sum('total_amt'))
    t_payment = Payment_Entry.objects.select_related().count()
    t_purchase = Purchase.objects.select_related().count()
    t_p_sale = PurchaseItem.objects.values_list().aggregate(Sum('total_amt'))

    t_item = ItemDetail.objects.select_related().count()
    t_customer = Customer.objects.select_related().count()

    context = {'t_sale_invoice': t_sale_invoice, 't_sale': t_sale,
               't_payment': t_payment, 't_purchase': t_purchase,
               't_p_sale': t_p_sale, 't_item': t_item, 't_customer': t_customer,
               }

    return render(request, 'electro/index.html', context)


def base(request):
    return render(request, 'electro/base.html')


def loginPage(request):
    if request.user.is_authenticated:
        return redirect('electro/index.html')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('index')
            else:
                messages.info(request, 'Username Or Password is Incorrect')
                return render(request, 'electro/login.html')
        context = {}
        return render(request, 'electro/login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('login')


# repoerting
def sales_repoert(request):
    s_reports = SaleItem.objects.select_related()
    myFilter = Sales_Filter(request.GET, queryset=s_reports)
    s_reports = myFilter.qs

    context = {'s_reports': s_reports, 'myFilter': myFilter}
    return render(request, 'electro/reports/sales_report.html', context)


def purchase_report(request):
    p_reports = PurchaseItem.objects.select_related()
    myFilter = Purchase_Filter(request.GET, queryset=p_reports)
    p_reports = myFilter.qs

    context = {'p_reports': p_reports, 'myFilter': myFilter}
    return render(request, 'electro/reports/purchase_report.html', context)


def payment_report(request):
    payment_repoert = Payment_Entry.objects.select_related()
    myFilter = Purchase_Filter(request.GET, queryset=payment_repoert)
    payment_repoert = myFilter.qs

    context = {'payment_repoert': payment_repoert, 'myFilter': myFilter}
    return render(request, 'electro/reports/payment_report.html', context)


def stock_report(request):
    stock_report = Inventory.objects.select_related()

    context = {'stock_report': stock_report}
    return render(request, 'electro/reports/stock_report.html', context)
