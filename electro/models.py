from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Sum
from django.utils.crypto import get_random_string
import secrets


# Vendor
class Vendor(models.Model):
    full_name = models.CharField(max_length=50)
    # photo = models.ImageField(upload_to="vendor/")
    address = models.TextField(blank=True)
    mobile = models.CharField(max_length=15, blank=True)
    status = models.BooleanField(default=False, blank=True)
    note = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = '1. کۆمپانیاکان'

    def __str__(self):
        return self.full_name


# Customer
class Customer(models.Model):
    customer_name = models.CharField(max_length=50, blank=True)
    customer_mobile = models.CharField(max_length=50, blank=True)
    customer_address = models.TextField(blank=True)
    city = models.CharField(max_length=50, blank=True)

    class Meta:
        verbose_name_plural = '2. کڕیار'

    def __str__(self):
        return self.customer_name


class SaleInvoice(models.Model):
    STATUS = (
        ('مدفوع', 'مدفوع'),
        ('غير مدفوع', 'غير مدفوع'),
        ('قسط ', ' قسط'),
    )
    invoice_number = models.CharField(unique=True, editable=False, max_length=10)

    customer_name = models.ForeignKey(Customer, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS, default='مدفوع')
    date = models.DateTimeField()
    note = models.CharField(max_length=100, blank=True)

    class Meta:
        verbose_name_plural = '3. پسولەی فرۆشتن'

    def save(self, *args, **kwargs):
        if not self.invoice_number:
            # Get the highest existing invoice number
            highest = SaleInvoice.objects.aggregate(models.Max('invoice_number'))['invoice_number__max']
            if highest is None:
                # If no invoices exist yet, start at 100
                self.invoice_number = 'SINV-100'
            else:
                # Increment the highest invoice number by 1 and add prefix
                prefix, number = highest.split('-')
                self.invoice_number = prefix + '-' + str(int(number) + 1)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.customer_name} - {self.invoice_number} - {self.total_sales_amount()}"

    def total_sales_amount(self):
        total_sales_amount = self.saleitem_set.aggregate(total=Sum('total_amt'))['total']
        return total_sales_amount or 0

    def total_sub_amount(self):
        total_sales_amount = self.saleitem_set.aggregate(total=Sum('sub_total'))['total']
        return total_sales_amount or 0

    def total_discount_amount(self):
        total_discount_amount = self.saleitem_set.aggregate(total=Sum('discount_value'))['total']
        return total_discount_amount or 0


class Payment_Entry(models.Model):
    Qst = (
        ('نقد', 'نقد'),
        ('قستی ١', 'قستی ١'),
        ('قستی ٢', 'قستی ٢'),
        ('قستی ٣ ', ' قستی ٣'),
        ('قستی ٤', 'قستی ٤'),
        ('قستی ٥', 'قستی ٥'),
        ('قستی ٦ ', ' قستی ٦'),
        ('قستی ٧', 'قستی ٧'),
        ('قستی ٨', 'قستی ٨'),
        ('قستی ٩ ', ' قستی ٩'),
        ('قستی ١٠', 'قستی ١٠'),
        ('قستی ١١', 'قستی ١١'),
        ('قستی ١٢ ', ' قستی ١٢'),
    )

    invoice_number = models.CharField(unique=True, editable=False, max_length=10)
    sales_invoice = models.ForeignKey(SaleInvoice, on_delete=models.CASCADE)
    # customer_name = models.ForeignKey(Customer, on_delete=models.CASCADE)
    q_type = models.CharField(max_length=10, verbose_name="Payment type", choices=Qst, blank=False)

    paid_amount = models.PositiveIntegerField(blank=False, default=1)
    payment_date = models.DateTimeField(blank=False)
    note = models.CharField(max_length=100, blank=True)
    old_balance = models.DecimalField(max_digits=20, decimal_places=2, default=0, editable=False)



    class Meta:
        verbose_name_plural = '8. پارەدان'

    def __str__(self):
        return str(self.invoice_number)

    def clean(self):
        if not self.q_type:
            raise ValidationError(' تکایە شێوازی پارەدان هەڵبژێرە؟')

    def save(self, *args, **kwargs):
        if not self.invoice_number:
            # Get the highest existing invoice number
            highest = Payment_Entry.objects.aggregate(models.Max('invoice_number'))['invoice_number__max']
            if highest is None:
                # If no invoices exist yet, start at 100
                self.invoice_number = 'PINV-100'
            else:
                # Increment the highest invoice number by 1 and add prefix
                prefix, number = highest.split('-')
                self.invoice_number = prefix + '-' + str(int(number) + 1)
        super().save(*args, **kwargs)
# Sales Invoice


# Unit


class Unit(models.Model):
    title = models.CharField(max_length=50)
    short_name = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = '5. یەکەی پێوان'

    def __str__(self):
        return self.title


# Item Details
class Item(models.Model):
    PRICELIST = (
        ('مفرد', 'مفرد'),
        ('جملة', 'جملة'),

        ('شراء', 'شراء'),
        ('قسط', 'قسط'),
    )

    name = models.CharField(max_length=255)
    price = models.PositiveIntegerField(default=1)
    price_list = models.CharField(max_length=8, choices=PRICELIST, default='مفرد')

    class Meta:
        verbose_name_plural = 'مواد'

    def __str__(self):
        return f"{self.name} - {self.price} - {self.price_list}"


# class Price_List(models.Model):
#     price_list = models.CharField(max_length=50, blank=True)
#
#     def __str__(self):
#         return str(self.price_list)
#
#     class Meta:
#         verbose_name_plural = 'Price_List'
#
#
# # Price List
# class ItemPrice(models.Model):
#     # PRICELIST = (
#     #     ('مفرد', 'مفرد'),
#     #     ('جملة', 'جملة'),
#     #
#     #     ('شراء', 'شراء'),
#     # )
#
#     item = models.ForeignKey(Item, on_delete=models.CASCADE)
#     price_list = models.ForeignKey(Price_List, on_delete=models.CASCADE)
#     item_price = models.FloatField()
#
#     class Meta:
#         verbose_name_plural = '6. Item Price'
#
#     def __str__(self):
#         return f'{self.item_price},{self.price_list}'


# Purchase Invoice
class Purchase(models.Model):
    invoice_number = models.CharField(max_length=8, unique=True, editable=False)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    date = models.DateTimeField()

    class Meta:
        verbose_name_plural = '8. زیادکردن بۆ کۆگا'

    def save(self, *args, **kwargs):
        if not self.invoice_number:
            # Generate a random 8 character invoice number
            self.invoice_number = secrets.token_hex(4).upper()
        super().save(*args, **kwargs)

    def clean(self):
        if PurchaseItem.item is None:
            raise ValidationError('Please select an Item')

    def __str__(self):
        return f' {self.invoice_number}'

    def total_purchase_amount(self):
        total_purchase_amount = self.purchaseitem_set.aggregate(total=Sum('total_amt'))['total']
        return total_purchase_amount or 0


# payment entry


# Sales Item
class SaleItem(models.Model):
    sales_invoice = models.ForeignKey(SaleInvoice, on_delete=models.CASCADE)

    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    qty = models.PositiveSmallIntegerField(default=1)
    # item_price = models.ForeignKey(ItemPrice, on_delete=models.CASCADE)
    # price = models.FloatField()
    sub_total = models.FloatField(editable=False, default=0)
    total_amt = models.FloatField(editable=False, default=0)
    sale_date = models.DateTimeField(auto_now_add=True)
    discount_type = models.CharField(max_length=10, choices=(
        ('amount', 'Amount'),
        ('percentage', 'Percentage')
    ), blank=True)
    discount_value = models.FloatField(blank=True, null=True)

    def save(self, *args, **kwargs):
        self.sub_total = self.item.price * self.qty
        if self.discount_type == 'amount' and self.discount_value is not None:
            discount = self.discount_value
        elif self.discount_type == 'percentage' and self.discount_value is not None:
            discount = self.item.price * self.discount_value / 100
        else:
            discount = 0

        self.total_amt = (self.qty * self.item.price) - discount

        super(SaleItem, self).save(*args, **kwargs)

        try:
            inventory = Inventory.objects.filter(item__name=self.item.name).latest('id')
        except Inventory.DoesNotExist:
            raise ValueError(f"{self.item.name} is not in stock")

        totalBal = inventory.total_bal_qty
        if self.qty > totalBal:
            raise ValueError(
                f"Sorry, we don't have enough {self.item.name} in stock right now. "
                f"Please reduce your sale quantity to {totalBal} or less."
            )

        inventory = Inventory.objects.filter(item__name=self.item.name).order_by('-id').first()
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

    def clean(self):
        if self.item.price_list != 'مفرد':
            raise ValidationError('Price list should  be " مفرد or جملة"')
        if not self.discount_type and self.discount_value:
            raise ValidationError('Please select a discount type')

    class Meta:
        verbose_name_plural = '9. Sales Item'


# Purchased Item
class PurchaseItem(models.Model):
    purchase_invoice = models.ForeignKey(Purchase, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    qty = models.FloatField()
    # item_price = models.ForeignKey(ItemPrice, on_delete=models.CASCADE)
    # price = models.FloatField()
    total_amt = models.FloatField(editable=False, default=0)
    pur_date = models.DateTimeField(auto_now_add=True)
    note = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        self.total_amt = self.qty * self.item.price
        super(PurchaseItem, self).save(*args, **kwargs)

        inventory = Inventory.objects.filter(item__name=self.item.name).order_by('-id').first()
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

    def clean(self):
        if self.item.price_list != 'شراء':
            raise ValidationError('Price list should be "شراء"')

    class Meta:
        verbose_name_plural = '9. Purchased Item'


# Inventories
class Inventory(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE, default=0, null=True)
    sale = models.ForeignKey(SaleInvoice, on_delete=models.CASCADE, default=0, null=True)
    pur_qty = models.FloatField(default=0, null=True)
    sale_qty = models.FloatField(default=0, null=True)
    total_bal_qty = models.FloatField(default=0)

    class Meta:
        verbose_name_plural = '10. زانیاری کۆگا'

    def __str__(self):
        return str(self.item)
