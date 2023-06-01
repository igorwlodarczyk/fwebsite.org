from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Subquery, Max
from .models import Item, ScrapedData, Url, Image, LowestPrice, PLN, EUR
from django.shortcuts import render, get_object_or_404
from django.utils import timezone

# Create your views here.


def index(request):
    currency_rates = get_currency_rates()
    sorted_items = get_all_items_sorted()
    items = Item.objects.all()
    for item in items:
        lowest_scraped_price = get_item_lowest_scraped_price(item)
        if lowest_scraped_price:
            lowest_price, currency = convert_currency(
                lowest_scraped_price.price,
                lowest_scraped_price.currency,
                currency_rates,
            )
        else:
            lowest_price = 9999
            currency = "USD"
        if lowest_scraped_price:
            update_lowest_price_table(latest_lowest_data=lowest_scraped_price)
        percentage_change = get_percentage_change(item=item)
        try:
            item.image = Image.objects.get(item=item).image_file
        except ObjectDoesNotExist:
            item.image = None
        finally:
            item.latest_lowest_price = lowest_price
            item.currency = currency
            item.percentage_change = percentage_change

    context = {"items": items, "sorted_items": sorted_items}
    return render(request, "fucking_scraper/home.html", context)


def all_items(request):
    currency_rates = get_currency_rates()
    sorted_items = get_all_items_sorted()
    items = Item.objects.all()
    for item in items:
        lowest_scraped_price = get_item_lowest_scraped_price(item)
        if lowest_scraped_price:
            lowest_price, currency = convert_currency(
                lowest_scraped_price.price,
                lowest_scraped_price.currency,
                currency_rates,
            )
        else:
            lowest_price = 9999
            currency = "USD"
        if lowest_scraped_price:
            update_lowest_price_table(latest_lowest_data=lowest_scraped_price)
        percentage_change = get_percentage_change(item=item)
        try:
            item.image = Image.objects.get(item=item).image_file
        except ObjectDoesNotExist:
            item.image = None
        finally:
            item.latest_lowest_price = lowest_price
            item.currency = currency
            item.percentage_change = percentage_change

    context = {"items": items, "sorted_items": sorted_items}
    return render(request, "fucking_scraper/all_items.html", context)


def item_detail(request, slug):
    currency_rates = get_currency_rates()
    item = get_object_or_404(Item, slug=slug)
    filtered_records = get_filtered_size_records(item)

    lowest_scraped_price = get_item_lowest_scraped_price(item)
    if lowest_scraped_price:
        lowest_price, currency = convert_currency(
            lowest_scraped_price.price, lowest_scraped_price.currency, currency_rates
        )
    else:
        lowest_price = 9999
        currency = "USD"
    if lowest_scraped_price:
        update_lowest_price_table(latest_lowest_data=lowest_scraped_price)
    percentage_change = get_percentage_change(item=item)
    last_updated = get_last_update_time(item)
    try:
        item.image = Image.objects.get(item=item).image_file
    except ObjectDoesNotExist:
        item.image = None
    finally:
        item.latest_lowest_price = lowest_price
        item.currency = currency
        item.percentage_change = percentage_change
        item.last_updated = last_updated

    if filtered_records:
        try:
            filtered_records = sorted(
                filtered_records, key=lambda record: float(record.size)
            )
        except ValueError:
            filtered_records = sorted(filtered_records, key=size_sort_key)

    context = {
        "item": item,
        "size_records": filtered_records,
    }
    return render(request, "fucking_scraper/item_detail.html", context)


def about_page(request):
    return render(request, "fucking_scraper/about_page.html")


def get_all_items_sorted():
    """
    Retrieve and return all items from the database, sorted by brand and model.

    :return: A queryset containing all items sorted by brand and model.
    :rtype: django.db.models.query.QuerySet
    """
    sorted_items = Item.objects.order_by("brand", "model")
    return sorted_items


def get_item_lowest_scraped_price(item):
    """
    Retrieves the latest scraped data for the lowest recorded price of a given item.

    :param item: The item for which to retrieve the lowest scraped price.
    :return: The latest scraped data object representing the lowest recorded price for the item.
             Returns None if there is no scraped data available for the item.
    """
    try:
        urls = Url.objects.filter(item=item)
        currency_rates = get_currency_rates()
        latest_data = []
        for url in urls:
            latest_data.append(
                ScrapedData.objects.filter(url=url).order_by("-date").first()
            )
        if latest_data:
            min_price_usd = float("inf")
            latest_lowest_data = None
            for data in latest_data:
                price_usd = convert_currency(data.price, data.currency, currency_rates)[
                    0
                ]
                if price_usd < min_price_usd:
                    min_price_usd = price_usd
                    latest_lowest_data = data
        else:
            latest_lowest_data = None
    except:
        latest_lowest_data = None

    return latest_lowest_data


def update_lowest_price_table(latest_lowest_data):
    """
    Updates the LowestPrice table with the latest lowest recorded price data.

    :param latest_lowest_data: The latest scraped data object representing the lowest recorded price.
    :return: None.
    """
    currency_rates = get_currency_rates()
    latest_lowest_price, currency = convert_currency(
        latest_lowest_data.price, latest_lowest_data.currency, currency_rates
    )
    try:
        lowest_recorded_price = (
            LowestPrice.objects.filter(item=latest_lowest_data.item)
            .order_by("-pk")
            .all()[0]
        )
        if latest_lowest_price != lowest_recorded_price.price:
            new_lowest_price = LowestPrice(
                price=latest_lowest_price,
                item=latest_lowest_data.item,
                date=latest_lowest_data.date,
            )
            new_lowest_price.save()
    except IndexError:
        if latest_lowest_data:
            new_lowest_price = LowestPrice(
                price=latest_lowest_price,
                item=latest_lowest_data.item,
                date=latest_lowest_data.date,
            )
            new_lowest_price.save()


def get_percentage_change(item):
    """
    Calculates the percentage change between the two lowest recorded prices for a given item.

    :param item: The item for which to calculate the percentage change.
    :return: The percentage change between the lowest and second-lowest recorded prices as a float.
             Returns 0 if there are fewer than two recorded prices for the item.
    """
    try:
        lowest_recorded_price = (
            LowestPrice.objects.filter(item=item).order_by("-pk").all()[0]
        )
        second_lowest_recorded_price = (
            LowestPrice.objects.filter(item=item).order_by("-pk").all()[1]
        )
        percentage_change = round(
            (lowest_recorded_price.price - second_lowest_recorded_price.price)
            / second_lowest_recorded_price.price
            * 100,
            2,
        )
        return percentage_change
    except IndexError:
        return 0


def get_filtered_size_records(item):
    """
    Retrieves the filtered size records for a given item.

    :param item: The item for which to retrieve the filtered size records.
    :return: A list of scraped data objects representing the lowest recorded price for each unique size of the item.
    """
    currency_rates = get_currency_rates()
    latest_scraped_data = (
        ScrapedData.objects.filter(item=item)
        .values("url_id")
        .annotate(max_date=Max("date"))
    )
    latest_records = ScrapedData.objects.filter(
        item=item,
        date__in=Subquery(latest_scraped_data.values("max_date")),
        url_id__in=Subquery(latest_scraped_data.values("url_id")),
    )

    filtered_records = []
    for size in set(latest_records.values_list("size", flat=True)):
        size_records = latest_records.filter(size=size)
        min_price_usd = float("inf")
        min_record = None
        for record in size_records:
            price_usd = convert_currency(record.price, record.currency, currency_rates)[
                0
            ]
            if price_usd < min_price_usd:
                min_price_usd = price_usd
                min_record = record
        min_record.price, min_record.currency = convert_currency(
            record.price, record.currency, currency_rates
        )
        url_obj = min_record.url
        min_record.store_name = url_obj.store_name
        min_record.item_url = url_obj.url
        filtered_records.append(min_record)
    return filtered_records


def get_last_update_time(item):
    """
    Retrieves the time difference between the current time and the date of the last recorded price for the given item.

    :param item: The item for which to retrieve the last update time.
    :return: A formatted string representation of the time difference between the current time and the last recorded price.
             Returns None if no recorded price is found for the item.
    """
    try:
        lowest_recorded_price = (
            ScrapedData.objects.filter(item=item).order_by("-pk").all()[0]
        )
        time_difference = timezone.now() - lowest_recorded_price.date
        return format_time_difference(time_difference)
    except IndexError:
        return None


def format_time_difference(time_difference):
    """
    Formats a time difference object into a human-readable string representation.

    :param time_difference: The time difference object to format, of type datetime.timedelta.
    :return: A formatted string representation of the time difference.
    """
    days = time_difference.days
    hours, remainder = divmod(time_difference.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    formatted_time = ""
    if days > 0:
        if days == 1:
            formatted_time += "1 day, "
        else:
            formatted_time += f"{days} days, "
    if hours > 0:
        if hours == 1:
            formatted_time += "1 hour, "
        else:
            formatted_time += f"{hours} hours, "
    if minutes > 0:
        if minutes == 1:
            formatted_time += "1 minute, "
        else:
            formatted_time += f"{minutes} minutes, "
    if seconds > 0:
        if seconds == 1:
            formatted_time += "1 second"
        else:
            formatted_time += f"{seconds} seconds"
    return formatted_time.rstrip(", ")


def get_currency_rates() -> dict:
    """
    Retrieves the latest currency rates for PLN, EUR, and USD.

    :return: A dictionary containing the latest currency rates. The keys are currency codes (PLN, EUR, USD),
             and the values are the corresponding exchange rates.
    """
    latest_pln_record = PLN.objects.latest("date")
    latest_pln_rate = latest_pln_record.pln_rate

    latest_eur_record = EUR.objects.latest("date")
    latest_eur_rate = latest_eur_record.eur_rate

    currency_rates = {"PLN": latest_pln_rate, "EUR": latest_eur_rate, "USD": 1}
    return currency_rates


def convert_currency(
    input_amount: float,
    from_currency: str,
    currency_rates: dict,
    to_currency: str = "USD",
) -> tuple:
    """
    Converts an input amount from one currency to another using the provided currency rates.

    :param input_amount: The amount to convert, as a float or an integer.
    :param from_currency: The currency code of the input amount.
    :param currency_rates: A dictionary containing currency rates. The keys are currency codes, and the values are
                           corresponding exchange rates.
    :param to_currency: The currency code to convert to. Default is "USD".
    :return: A tuple containing the converted amount and the currency code it was converted to.
    """
    return round(input_amount / (currency_rates[from_currency]), 2), to_currency


def size_sort_key(size: str) -> int:
    """
    Returns the sorting key for a given size string.

    :param size: The size string to determine the sorting key for.
    :return: The sorting key as an integer.
    """
    size_order = {
        "XS": 0,
        "S": 1,
        "M": 2,
        "L": 3,
        "XL": 4,
        "XXL": 5,
        "2XL": 5,
        "XXXL": 6,
        "3XL": 6,
        "XXXXL": 7,
        "4XL": 7,
    }
    return size_order.get(size, 8)
