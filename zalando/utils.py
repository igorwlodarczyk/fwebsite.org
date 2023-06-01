import zalando.constants as const
from typing import Union


def parse_sizes(sizes: Union[str, list]) -> list:
    """
    Parses the given sizes and returns a list of parsed sizes.

    :param sizes: A string or a list of sizes to be parsed.
                  If a string is provided, it will be converted into a list with a single element.
    :return: A list of parsed sizes.

    The function takes a single size or a list of sizes as input and parses them. If the input is a string,
    it will be converted into a list with a single element before parsing. The parsing process involves
    removing any newline characters from each size element. The resulting parsed sizes are stored in a list
    and returned.
    """
    if not isinstance(sizes, list):
        sizes = [sizes]
    parsed_sizes = []
    for size in sizes:
        if "\n" in size:
            parsed_sizes.append(size.split("\n")[0])
        else:
            parsed_sizes.append(size)
    return parsed_sizes


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
