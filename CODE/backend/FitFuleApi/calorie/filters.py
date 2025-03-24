import django_filters
from .models import Product


class ProductFilter(django_filters.FilterSet):
    ids = django_filters.CharFilter(method='filter_by_ids')

    class Meta:
        model = Product
        fields = ['ids']

    def filter_by_ids(self, queryset, name, value):
        ids = value.split(',')
        return queryset.filter(id__in=ids)
