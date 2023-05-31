from django_filters import rest_framework as filters

from .models import Store


class StoreFilter(filters.FilterSet):

    class Meta:
        model = Store
        fields = '__all__'

