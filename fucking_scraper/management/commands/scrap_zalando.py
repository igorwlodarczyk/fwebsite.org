from django.core.management import BaseCommand
from fucking_scraper.models import Url, ScrapedData
from scrapers.zalando.scraper import get_data


class Command(BaseCommand):
    def handle(self, *args, **options):
        zalando_urls = Url.objects.filter(store_name__startswith="Zalando").values_list(
            "url", flat=True
        )
        for url in zalando_urls:
            try:
                price, sizes, date, currency = get_data(url)
            except Exception:
                price = None
                sizes = None
                date = None
                currency = None
            if all((price, sizes, date, currency)):
                item = Url.objects.filter(url=url).first().item
                scraped_url = Url.objects.filter(url=url).first()
                for size in sizes:
                    scraped_data = ScrapedData(
                        price=price,
                        currency=currency,
                        size=size,
                        date=date,
                        item=item,
                        url=scraped_url,
                    )
                    scraped_data.save()
