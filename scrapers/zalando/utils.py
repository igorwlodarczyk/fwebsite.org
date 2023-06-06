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
    """
    Detects shoe sizes and parses them from EU measurement to US measurement.

    :param sizes: The sizes to be detected and parsed. It can be either a list of strings or a single string.
    :return: The parsed sizes as a list of strings.

    If the input `sizes` is a string, it is parsed into a list of sizes using the `parse_sizes` function.
    Each size in the list is converted from EU measurement to US measurement using the `convert_size_eu_to_us` function.
    The converted sizes are stored in a new list `parsed_sizes`, which is returned as the result.

    If any error occurs during the conversion (e.g., invalid input size), the original sizes are returned as is.

    Example:
    >>> detect_shoe_sizes_and_parse(["42.5", "38", "39.5"])
    ['9.0', '5.0', '6.5']
    >>> detect_shoe_sizes_and_parse("41.5 37 40")
    ['8.5', '5.0', '7.0']
    >>> detect_shoe_sizes_and_parse(["45.5", "abc", "39"])
    ['11.5', 'abc', '6.0']
    """
    sizes = parse_sizes(sizes)
    parsed_sizes = []
    try:
        for size in sizes:
            parsed_size = convert_size_eu_to_us(float(size))
            parsed_sizes.append(str(parsed_size))
        return parsed_sizes
    except ValueError:
        return sizes
