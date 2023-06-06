from scrapers.zalando import constants as const
from common.utils import convert_size_eu_to_us, parse_sizes
from typing import Union


def get_currency(url: str) -> str:
    """
    Retrieves the currency associated with a given URL.
    :param url: The URL for which the currency needs to be determined.
    :return: The currency code (e.g., "USD", "EUR") associated with the URL, or None if no matching currency is found.
    """
    for zalando_url in const.currency.keys():
        if zalando_url in url:
            return const.currency[zalando_url]
    return None


def detect_shoe_sizes_and_parse(sizes: Union[list, str]) -> list:
    sizes = parse_sizes(sizes)
    parsed_sizes = []
    try:
        for size in sizes:
            parsed_size = convert_size_eu_to_us(float(size))
            parsed_sizes.append(str(parsed_size))
        return parsed_sizes
    except ValueError:
        return sizes
