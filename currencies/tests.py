import responses

from django.core.management import call_command
from django.test import TestCase

from currencies.models import CurrencyRate
from exchange_rates_app import settings


class TestCurrencyRate(TestCase):

    @classmethod
    @responses.activate
    def setUpTestData(cls):
        responses.add(
            responses.GET,
            'https://www.ecb.europa.eu/stats/eurofxref/eurofxref-daily.xml',
            body=open('scraper/test_data/eurofxref-daily.xml').read(),
        )
        call_command('update_rates')

    def test_get_single_unit_of_currency_in_base_currency(self):
        usd = CurrencyRate.objects.get(currency_symbol='USD')
        self.assertEqual(
            round(
                usd.get_single_unit_of_currency_in_base_currency,
                settings.DECIMAL_PLACES_PRECISION
            ),
            0.87497
        )

    def test_get_single_unit_of_currency_in_base_currency_2(self):
        pln = CurrencyRate.objects.get(currency_symbol='PLN')
        self.assertEqual(
            round(
                pln.get_single_unit_of_currency_in_base_currency,
                settings.DECIMAL_PLACES_PRECISION
            ),
            0.23307
        )

    def test_get_amount_of_currency_in_base_currency(self):
        pln = CurrencyRate.objects.get(currency_symbol='PLN')
        self.assertEqual(
            pln.get_amount_of_currency_in_base_currency(42905),
            10000.0
        )
        self.assertEqual(
            round(pln.get_amount_of_currency_in_base_currency(1000),
                  settings.DECIMAL_PLACES_PRECISION
            ),
            233.07307
        )

    def test_get_amount_of_base_currency_in_currency(self):
        pln = CurrencyRate.objects.get(currency_symbol='PLN')
        self.assertEqual(
            pln.get_amount_of_base_currency_in_currency(10000),
            42905
        )
