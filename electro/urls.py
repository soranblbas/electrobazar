from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('login', views.loginPage, name="login"),
    path('logout', views.logoutUser, name="logout"),
    path('base', views.base, name="base"),

    # REPORTS

    path('sales_report', views.sales_repoert, name="sales_report"),
    path('purchase_report', views.purchase_repoert, name="purchase_report"),

]
