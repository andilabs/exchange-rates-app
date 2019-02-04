from django.conf import settings
from iso4217 import raw_table
from rest_framework import serializers
from rest_framework.exceptions import NotFound
from currencies.models import CurrencyRate

all_currencies_codes = list(raw_table.keys())
all_currencies_codes.remove('ALL')


class CurrencyField(serializers.Field):

    def to_representation(self, value):
        return value

    def to_internal_value(self, data):
        if data not in all_currencies_codes:
            raise serializers.ValidationError(
                'Invalid currency code: {}'.format(data))
        try:
            currency = CurrencyRate.objects.get(currency_symbol=data)
        except CurrencyRate.DoesNotExist:
            raise NotFound(
                'Sorry, but we do not handle yet {} currency'.format(data))

        return currency


class CurrencyRateConverterSerializer(serializers.Serializer):
    input_base_currency = CurrencyField(write_only=True)
    input_target_currency = CurrencyField(write_only=True)
    base_amount = serializers.FloatField(write_only=True)

    converted_amount = serializers.FloatField(read_only=True)

    def validate(self, attrs):
        amount = attrs.get('base_amount')
        input_base_currency = attrs.get('input_base_currency')
        base_currency_amount = input_base_currency.get_amount_of_currency_in_base_currency(
            amount
        )
        input_target_currency = attrs.get('input_target_currency')
        target_currency_amount = input_target_currency.get_amount_of_base_currency_in_currency(
            base_currency_amount
        )
        attrs['converted_amount'] = round(
            target_currency_amount, settings.DECIMAL_PLACES_PRECISION)
        return attrs
