from iso4217 import raw_table

from django.db import models
from django.conf import settings

all_currencies_codes = [(iso_code, value['CcyNm']) for iso_code, value in raw_table.items()]


class TimeStampedModel(models.Model):

    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True, db_index=True)

    class Meta:
        abstract = True


class CurrencyRate(TimeStampedModel):

    for_date = models.DateField()
    currency_symbol = models.CharField(max_length=3,
                                       choices=all_currencies_codes)
    rate = models.FloatField()
    base_currency = models.CharField(
        default=settings.BASE_CURRENCY,
        max_length=3,
        choices=all_currencies_codes
    )

    class Meta:
        unique_together = (
            'for_date', 'currency_symbol', 'rate', 'base_currency'
        )

    def __str__(self):
        return "1{} = {}{}".format(
            self.base_currency,
            self.rate,
            self.currency_symbol,
        )

    @property
    def get_single_unit_of_currency_in_base_currency(self):
        return 1.0 / self.rate

    def get_amount_of_currency_in_base_currency(self, amount):
        return amount * self.get_single_unit_of_currency_in_base_currency

    def get_amount_of_base_currency_in_currency(self, amount):
        return amount * self.rate
