import requests


def convert_currency_api(input_amount, from_currency, to_currency):
    """
    Converts an input amount from one currency to another using the Frankfurter API.

    :param input_amount: The amount to convert, as a float or an integer.
    :param from_currency: The currency code of the input amount.
    :param to_currency: The currency code to convert to.
    :return: The converted amount as a float rounded to 2 decimal places. Returns None if the conversion fails or an error occurs.
    """
    url = f"https://api.frankfurter.app/latest"
    params = {
        "amount": input_amount,
        "from": from_currency,
        "to": to_currency,
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        converted_amount = data["rates"][to_currency]
        return round(converted_amount, 2)
    else:
        return None


def get_usd_rate(currency):
    """
    Retrieves the exchange rate of the specified currency against the USD.

    :param currency: The currency code for which to retrieve the exchange rate.
    :return: The exchange rate of the specified currency against the USD. Returns None if the retrieval fails or an error occurs.
    """
    return convert_currency_api(1, "USD", currency)
