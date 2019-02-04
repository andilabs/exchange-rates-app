import responses

from django.core.management import call_command
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase


class TestCurrencyRateConverterApiView(APITestCase):

    @classmethod
    @responses.activate
    def setUpTestData(cls):
        responses.add(
            responses.GET,
            'https://www.ecb.europa.eu/stats/eurofxref/eurofxref-daily.xml',
            body=open('scraper/test_data/eurofxref-daily.xml').read(),
        )
        call_command('update_rates')

    def test_get_conversion_of_1_eur_to_pln(self):
        url = reverse(
            'api:currency-converter', kwargs={
                'base_currency_code': 'EUR',
                'target_currency_code': 'PLN',
                'amount': 1
            }
        )
        response = self.client.get(url)
        self.assertEqual(
            response.status_code, 200
        )
        self.assertEqual(
            response.json()['converted_amount'], 4.2905
        )

    def test_get_conversion_of_1000_pln_to_eur(self):
        url = reverse(
            'api:currency-converter', kwargs={
                'base_currency_code': 'PLN',
                'target_currency_code': 'EUR',
                'amount': 1000
            }
        )
        response = self.client.get(url)
        self.assertEqual(
            response.status_code, 200
        )
        self.assertEqual(
            response.json()['converted_amount'], 233.07307
        )

    def test_get_conversion_of_1000_pln_to_pln(self):
        url = reverse(
            'api:currency-converter', kwargs={
                'base_currency_code': 'PLN',
                'target_currency_code': 'PLN',
                'amount': 1000
            }
        )
        response = self.client.get(url)
        self.assertEqual(
            response.status_code, 200
        )
        self.assertEqual(
            response.json()['converted_amount'], 1000
        )
