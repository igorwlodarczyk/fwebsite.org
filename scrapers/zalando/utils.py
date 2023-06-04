from scrapers.zalando import constants as const


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
