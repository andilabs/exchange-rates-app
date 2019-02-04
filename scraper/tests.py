import responses
from django.test import TestCase

from currencies.models import CurrencyRate
from scraper.scraping import ECBCurrencyRatesScraper


class TestECBCurrencyRatesScraper(TestCase):

    @staticmethod
    def load_fixture():
        with open('scraper/test_data/eurofxref-daily.xml') as F:
            return F.read()

    @responses.activate
    def setUp(self):
        responses.add(
            responses.GET,
            'https://www.ecb.europa.eu/stats/eurofxref/eurofxref-daily.xml',
            body=self.load_fixture(),
        )
        self.scraper = ECBCurrencyRatesScraper()

    def test_parse_date(self):
        self.assertEqual(
            self.scraper.parse_date(),
            '2019-01-30'
        )

    def test_parse_rates(self):
        self.assertEqual(
            len(self.scraper.parse_rates()),
            32
        )
        self.assertEqual(
            type(self.scraper.parse_rates()[0]),
            dict
        )
        self.assertEqual(
            self.scraper.parse_rates()[0],
            {'currency': 'USD', 'rate': '1.1429'}
        )

    def test_parse_currency_rates(self):
        self.assertEqual(CurrencyRate.objects.count(), 0)
        self.scraper.parse_currency_rates()
        self.assertEqual(CurrencyRate.objects.count(), 32 + 1)
        self.assertEqual(
            str(CurrencyRate.objects.first().for_date), '2019-01-30'
        )
