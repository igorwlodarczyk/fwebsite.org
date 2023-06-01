from django.core.management import BaseCommand
from fucking_scraper.models import Url, ScrapedData
from zalando.scraper import get_data


class Command(BaseCommand):
    def handle(self, *args, **options):
        zalando_urls = Url.objects.filter(store_name__startswith="Zalando").values_list(
            "url", flat=True
        )
        for url in zalando_urls:
            price, sizes, date, currency = get_data(url)
            if (
                price is not None
                and sizes is not None
                and date is not None
                and currency is not None
            ):
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
