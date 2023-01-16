from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from electro.models import *
from django.contrib.auth import authenticate, login, logout


@login_required(login_url='login')
def index(request):
    return render(request, 'electro/index.html')


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

    context = {'s_reports':s_reports}
    return render(request, 'electro/reports/sales_report.html', context)
