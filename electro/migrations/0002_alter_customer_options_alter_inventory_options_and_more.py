# Generated by Django 4.2.5 on 2023-09-15 12:11

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('electro', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='customer',
            options={'verbose_name_plural': '2. کڕیار'},
        ),
        migrations.AlterModelOptions(
            name='inventory',
            options={'verbose_name_plural': '10. زانیاری کۆگا'},
        ),
        migrations.AlterModelOptions(
            name='payment_entry',
            options={'verbose_name_plural': '8. پارەدان'},
        ),
        migrations.AlterModelOptions(
            name='purchase',
            options={'verbose_name_plural': '8. زیادکردن بۆ کۆگا'},
        ),
        migrations.AlterModelOptions(
            name='saleinvoice',
            options={'verbose_name_plural': '3. پسولەی فرۆشتن'},
        ),
        migrations.AlterModelOptions(
            name='unit',
            options={'verbose_name_plural': '5. یەکەی پێوان'},
        ),
        migrations.AlterModelOptions(
            name='vendor',
            options={'verbose_name_plural': '1. کۆمپانیاکان'},
        ),
        migrations.RemoveField(
            model_name='payment_entry',
            name='customer_name',
        ),
        migrations.RemoveField(
            model_name='saleinvoice',
            name='piad',
        ),
        migrations.AddField(
            model_name='payment_entry',
            name='q_type',
            field=models.CharField(choices=[('نقد', 'نقد'), ('قستی ١', 'قستی ١'), ('قستی ٢', 'قستی ٢'), ('قستی ٣ ', ' قستی ٣'), ('قستی ٤', 'قستی ٤'), ('قستی ٥', 'قستی ٥'), ('قستی ٦ ', ' قستی ٦'), ('قستی ٧', 'قستی ٧'), ('قستی ٨', 'قستی ٨'), ('قستی ٩ ', ' قستی ٩'), ('قستی ١٠', 'قستی ١٠'), ('قستی ١١', 'قستی ١١'), ('قستی ١٢ ', ' قستی ١٢')], default=1, max_length=10, verbose_name='Payment type'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='saleinvoice',
            name='note',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='saleinvoice',
            name='status',
            field=models.CharField(choices=[('مدفوع', 'مدفوع'), ('غير مدفوع', 'غير مدفوع'), ('قسط ', ' قسط')], default='مدفوع', max_length=10),
        ),
        migrations.AddField(
            model_name='saleitem',
            name='discount_type',
            field=models.CharField(blank=True, choices=[('amount', 'Amount'), ('percentage', 'Percentage')], max_length=10),
        ),
        migrations.AddField(
            model_name='saleitem',
            name='discount_value',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='saleitem',
            name='sub_total',
            field=models.FloatField(default=0, validators=[django.core.validators.MinValueValidator(0.01)]),
        ),
        migrations.AlterField(
            model_name='item',
            name='price_list',
            field=models.CharField(choices=[('مفرد', 'مفرد'), ('جملة', 'جملة'), ('شراء', 'شراء'), ('قسط', 'قسط')], default='مفرد', max_length=8),
        ),
        migrations.AlterField(
            model_name='payment_entry',
            name='invoice_number',
            field=models.CharField(editable=False, max_length=10, unique=True),
        ),
        migrations.AlterField(
            model_name='payment_entry',
            name='note',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='payment_entry',
            name='paid_amount',
            field=models.FloatField(default=1, validators=[django.core.validators.MinValueValidator(0.01)]),
        ),
        migrations.AlterField(
            model_name='payment_entry',
            name='payment_date',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='purchase',
            name='invoice_number',
            field=models.CharField(editable=False, max_length=8, unique=True),
        ),
        migrations.AlterField(
            model_name='purchaseitem',
            name='note',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='purchaseitem',
            name='qty',
            field=models.FloatField(default=0, validators=[django.core.validators.MinValueValidator(0.01)]),
        ),
        migrations.AlterField(
            model_name='purchaseitem',
            name='total_amt',
            field=models.FloatField(default=0, editable=False, validators=[django.core.validators.MinValueValidator(0.01)]),
        ),
        migrations.AlterField(
            model_name='saleinvoice',
            name='invoice_number',
            field=models.CharField(editable=False, max_length=10, unique=True),
        ),
        migrations.AlterField(
            model_name='saleitem',
            name='total_amt',
            field=models.FloatField(default=0, editable=False, validators=[django.core.validators.MinValueValidator(0.01)]),
        ),
    ]
