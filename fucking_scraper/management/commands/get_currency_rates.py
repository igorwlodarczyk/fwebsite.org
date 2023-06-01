from django.core.management import BaseCommand
from fucking_scraper.models import PLN, EUR
from currency_api.common import get_usd_rate
from datetime import datetime


class Command(BaseCommand):
    def handle(self, *args, **options):
        """
        Fetches the USD exchange rate for EUR and PLN and saves them in the database.

        :param args: Additional positional arguments (unused)
        :param options: Additional keyword arguments (unused)
        :return: None
        """
        eur_rate = get_usd_rate("EUR")
        eur = EUR(eur_rate=eur_rate, date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        eur.save()

        pln_rate = get_usd_rate("PLN")
        pln = PLN(pln_rate=pln_rate, date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        pln.save()
