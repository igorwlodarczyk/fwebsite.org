from pathlib import Path
import os
import re


def clear_debug_logs(debug_logs_path=None):
    """
    Removes all debug logs that do not contain the string "Error".

    This function searches for all files in the current directory whose filename contains the word "debug".
    If a file is found, its contents are checked for the presence of the word "Error".
    If the word "Error" is not found in the file, the file is deleted.
    :return: None
    """
    if debug_logs_path is None:
        file_path = Path().absolute()
    else:
        file_path = debug_logs_path

    for file in file_path.iterdir():
        filename = os.path.basename(file)
        if "debug" in filename:
            with open(file) as f:
                file_content = f.read()
                if "Error" not in file_content:
                    os.remove(file)


def parse_price(price: str) -> float:
    """
    Converts a string representing a price to a floating-point number.
    :param price: A string representing the price.
    :return: A float representing the price.
    """
    price = re.sub(r"[^0-9.,]", "", price)
    price = price.replace(",", ".")
    return float(price)
