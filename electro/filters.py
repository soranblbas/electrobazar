import django_filters
from django_filters import DateFilter
from .models import *


class Sales_Filter(django_filters.FilterSet):
    max_date = DateFilter(field_name='sale_date', lookup_expr='gte')
    min_date = DateFilter(field_name='sale_date', lookup_expr='lte')

    class Meta:
        model = SaleItem
        fields = ['min_date', 'max_date']
        exclude = ['sale_date']
