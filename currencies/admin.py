from django.contrib import admin

from currencies.models import CurrencyRate


@admin.register(CurrencyRate)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = ('for_date', 'currency_symbol', 'rate', 'base_currency')
