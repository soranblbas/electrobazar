from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Sum
from django.utils.crypto import get_random_string


# Vendor
class Vendor(models.Model):
    full_name = models.CharField(max_length=50)
    # photo = models.ImageField(upload_to="vendor/")
    address = models.TextField(blank=True)
    mobile = models.CharField(max_length=15, blank=True)
    status = models.BooleanField(default=False, blank=True)
    note = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = '1. Vendors'

    def __str__(self):
        return self.full_name


# Customer
class Customer(models.Model):
    customer_name = models.CharField(max_length=50, blank=True)
    customer_mobile = models.CharField(max_length=50, blank=True)
    customer_address = models.TextField(blank=True)
    city = models.CharField(max_length=50, blank=True)

    class Meta:
        verbose_name_plural = '2. Customers'

    def __str__(self):
        return self.customer_name


class SaleInvoice(models.Model):
    STATUS = (
        ('مدفوع', 'مدفوع'),
        ('غير مدفوع', 'غير مدفوع'),
    )
    invoice_number = models.SlugField(editable=False)
    customer_name = models.ForeignKey(Customer, on_delete=models.CASCADE)
    piad = models.BooleanField(default='No')
    date = models.DateTimeField()

    class Meta:
        verbose_name_plural = '3. Sale Invoice'

    def save(self, *args, **kwargs):
        CODE_LENGTH = 5
        #
        # # self.p_search = '-'.join((slugify(self.project_name),))
        self.invoice_number = 'SINV-' + get_random_string(CODE_LENGTH).upper()

        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.invoice_number)


class Payment_Entry(models.Model):
    invoice_number = models.SlugField(editable=False)
    sales_invoice = models.ForeignKey(SaleInvoice, on_delete=models.CASCADE)
    customer_name = models.ForeignKey(Customer, on_delete=models.CASCADE)

    paid_amount = models.FloatField(blank=True)
    payment_date = models.DateTimeField(blank=True)
    note = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        CODE_LENGTH = 5

        # self.p_search = '-'.join((slugify(self.project_name),))
        self.invoice_number = 'PINV-' + get_random_string(CODE_LENGTH).upper()

        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = '8. Payment Entry'

    def __str__(self):
        return str(self.sales_invoice.invoice_number)


# Sales Invoice


# Unit


class Unit(models.Model):
    title = models.CharField(max_length=50)
    short_name = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = '5. Units'

    def __str__(self):
        return self.title


# Item Details
class ItemDetail(models.Model):
    title = models.CharField(max_length=50)
    detail = models.TextField(blank=True)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)

    # photo = models.ImageField(upload_to="product/")
    class Meta:
        verbose_name_plural = '7. Items Detail'

    def __str__(self):
        return self.title


class Price_List(models.Model):
    price_list = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return str(self.price_list)

    class Meta:
        verbose_name_plural = 'Price_List'


# Price List
class ItemPrice(models.Model):
    # PRICELIST = (
    #     ('مفرد', 'مفرد'),
    #     ('جملة', 'جملة'),
    #
    #     ('شراء', 'شراء'),
    # )

    item = models.ForeignKey(ItemDetail, on_delete=models.CASCADE)
    price_list = models.ForeignKey(Price_List, on_delete=models.CASCADE)
    item_price = models.FloatField()

    class Meta:
        verbose_name_plural = '6. Item Price'

    def __str__(self):
        return f'{self.item_price},{self.price_list}'


# Purchase Invoice
class Purchase(models.Model):
    invoice_number = models.SlugField(default=0)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    date = models.DateTimeField()

    class Meta:
        verbose_name_plural = '8. Purchase Invoice'

    def save(self, *args, **kwargs):
        CODE_LENGTH = 5

        # self.p_search = '-'.join((slugify(self.project_name),))
        self.invoice_number = 'PINV-' + get_random_string(CODE_LENGTH).upper()

        super().save(*args, **kwargs)

    def __str__(self):
        return f' {self.invoice_number}'


# payment entry


# Sales Item
class SaleItem(models.Model):
    sales_invoice = models.ForeignKey(SaleInvoice, on_delete=models.CASCADE)

    item = models.ForeignKey(ItemDetail, on_delete=models.CASCADE)
    qty = models.PositiveSmallIntegerField(default=1)
    item_price = models.ForeignKey(ItemPrice, on_delete=models.CASCADE)
    # price = models.FloatField()
    total_amt = models.FloatField(editable=False, default=0)
    sale_date = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):

        self.total_amt = self.qty * self.item_price.item_price
        # self.total_amt = self.total_amt - self.payment_entry.paid_amount
        # item_in_stock = PurchaseItem.objects.filter(item=self.item).first()
        # if item_in_stock:
        #     raise ValidationError("Quantity cannot be greater than the stock amount.")

        super(SaleItem, self).save(*args, **kwargs)

        inventory = Inventory.objects.filter(item=self.item).order_by('-id').first()
        if inventory:
            totalBal = inventory.total_bal_qty - self.qty
        else:
            totalBal = 0

        Inventory.objects.create(
            item=self.item,
            purchase=None,
            sale=self.sales_invoice,
            pur_qty=None,
            sale_qty=self.qty,
            total_bal_qty=totalBal
        )

    class Meta:
        verbose_name_plural = '9. Sales Item'


# Purchased Item
class PurchaseItem(models.Model):
    purchase_invoice = models.ForeignKey(Purchase, on_delete=models.CASCADE)
    item = models.ForeignKey(ItemDetail, on_delete=models.CASCADE)
    qty = models.FloatField()
    item_price = models.ForeignKey(ItemPrice, on_delete=models.CASCADE)
    # price = models.FloatField()
    total_amt = models.FloatField(editable=False, default=0)
    pur_date = models.DateTimeField(auto_now_add=True)
    note = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        self.total_amt = self.qty * self.item_price.item_price
        super(PurchaseItem, self).save(*args, **kwargs)

        inventory = Inventory.objects.filter(item=self.item).order_by('-id').first()
        if inventory:
            totalBal = inventory.total_bal_qty + self.qty
        else:
            totalBal = self.qty
        Inventory.objects.create(
            item=self.item,
            purchase=self.purchase_invoice,
            sale=None,
            pur_qty=self.qty,
            sale_qty=None,
            total_bal_qty=totalBal
        )

    class Meta:
        verbose_name_plural = '9. Purchased Item'


# Inventories
class Inventory(models.Model):
    item = models.ForeignKey(ItemDetail, on_delete=models.CASCADE)
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE, default=0, null=True)
    sale = models.ForeignKey(SaleInvoice, on_delete=models.CASCADE, default=0, null=True)
    pur_qty = models.FloatField(default=0, null=True)
    sale_qty = models.FloatField(default=0, null=True)
    total_bal_qty = models.FloatField(default=0)

    class Meta:
        verbose_name_plural = '10. Stock Details'

    def __str__(self):
        return str(self.item)
