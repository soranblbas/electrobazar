from django.contrib import admin
from .models import *


# Register your models here.

class SalesItem(admin.TabularInline):
    model = SaleItem
    extra = 1


@admin.register(SaleInvoice)
class ProfileAdmin(admin.ModelAdmin):
    inlines = [SalesItem]

    class Meta:
        model = SaleInvoice


class PurchasesItem(admin.TabularInline):
    model = PurchaseItem
    extra = 1


@admin.register(Purchase)
class ProfileAdmin(admin.ModelAdmin):
    inlines = [PurchasesItem]

    class Meta:
        model = Purchase


@admin.register(ItemPrice)
class CustomerPagination(admin.ModelAdmin):
    list_display = ('item', 'price_list', 'item_price')
    # list_filter = ("client_name", "status", "date_created")
    # list_display_links = ('client_name',)
    # list_per_page = 20


# @admin.register(Purchase)
# class CustomerPagination(admin.ModelAdmin):
#     list_display = ('item', 'vendor', 'qty', 'price', 'total_amt', 'pur_date')
#     # list_filter = ("client_name", "status", "date_created")
#     # list_display_links = ('client_name',)
#     # list_per_page = 20
#     readonly_fields = ['total_amt', ]


@admin.register(PurchaseItem)
class CustomerPagination(admin.ModelAdmin):
    list_display = ('item', 'qty', 'item_price', 'total_amt', 'pur_date')

    readonly_fields = ['total_amt', ]


@admin.register(SaleItem)
class CustomerPagination(admin.ModelAdmin):
    list_display = ('item', 'qty', 'item_price', 'total_amt', 'sale_date')

    readonly_fields = ['total_amt', ]


@admin.register(Inventory)
class CustomerPagination(admin.ModelAdmin):
    list_display = ('item', 'purchase', 'sale','pur_qty', 'sale_qty', 'total_bal_qty')
    list_display_links = ['purchase', 'sale', ]


admin.site.register(Vendor)
admin.site.register(Unit)

admin.site.register(ItemDetail)

admin.site.register(Customer)
admin.site.register(Price_List)

