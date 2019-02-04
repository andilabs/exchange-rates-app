import requests
import xml.etree.ElementTree as ET

from django.conf import settings
from django.utils import dateparse

from currencies.models import CurrencyRate


class BaseCurrencyRatesScraper(object):
    data_url = NotImplementedError

    def get_data(self):
        response = requests.get(self.data_url)
        if response.status_code == 200:
            return response.content
        else:
            raise ValueError

    def parse_currency_rates(self):
        raise NotImplementedError


class ECBCurrencyRatesScraper(BaseCurrencyRatesScraper):
    data_url = "https://www.ecb.europa.eu/stats/eurofxref/eurofxref-daily.xml"
    namespaces = {'ecb': 'http://www.ecb.int/vocabulary/2002-08-01/eurofxref'}
    xml_data = None

    def parse_date(self):
        return self.xml_data.find(
            '*//ecb:Cube[@time]', namespaces=self.namespaces
        ).get('time')

    def parse_rates(self):
        return [dict(rate.items()) for rate in self.xml_data.findall(
            '*//ecb:Cube[@rate]', namespaces=self.namespaces
        )]

    def parse_currency_rates(self):
        for_date = self.parse_date()
        rates = self.parse_rates()
        created_count = 0
        for rate in rates:
            _, created = CurrencyRate.objects.update_or_create(
                currency_symbol=rate.get('currency'),
                defaults={
                    'for_date': dateparse.parse_date(for_date),
                    'rate': rate.get('rate')
                }
            )
            if created:
                created_count += 1
        _, created = CurrencyRate.objects.update_or_create(
            currency_symbol=settings.BASE_CURRENCY,
            defaults={
                'for_date': dateparse.parse_date(for_date),
                'rate': 1.0
            }
        )
        if created:
            created_count += 1
        print("Created: {}, Updated: {}".format(
            created_count, len(rates)+1-created_count))

    def __init__(self):
        self.xml_data = ET.ElementTree(ET.fromstring(self.get_data()))
