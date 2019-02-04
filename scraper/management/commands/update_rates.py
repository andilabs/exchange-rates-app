from django.core.management.base import BaseCommand

from scraper.scraping import ECBCurrencyRatesScraper


class Command(BaseCommand):

    def handle(self, *args, **options):
        ecb_parser = ECBCurrencyRatesScraper()
        ecb_parser.parse_currency_rates()
