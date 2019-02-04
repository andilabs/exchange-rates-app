from django_filters import rest_framework as filters

from currencies.models import CurrencyRate


class SpotFilterSet(filters.FilterSet):

    class Meta:
        model = CurrencyRate
        fields = [
            'currency_symbol'
        ]
