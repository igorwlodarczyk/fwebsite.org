import common.constants as const
import os
import re
import logging
import uuid
from datetime import datetime
from pathlib import Path
from typing import Union


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


def parse_size(size: str) -> str:
    """
    Parses a string representing a size and returns the standardized size value.
    :param size: A string representing the size.
    :return: A string representing the standardized size value.
    """
    for key in const.size_equivalents.keys():
        if key == size.upper():
            return const.size_equivalents[key]
    return size


def get_logger(store_name: str) -> logging.Logger:
    """
    Returns a logger object configured with a unique ID and file handler.

    :param store_name: The name of the store.
    :return: A logger object.

    Example usage:
    >>> logger = get_logger("my_store")
    >>> logger.debug("Debug message")
    >>> logger.info("Info message")
    """
    unique_id = str(uuid.uuid4())[:10]
    logger = logging.getLogger(f"{store_name}__{unique_id}")
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        "%(asctime)s %(levelname)s %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
    )
    log_file_name = (
        f"log_debug_{datetime.now().strftime('%Y-%m-%d_%H:%M:%S')}__{unique_id}"
    )
    file_handler = logging.FileHandler(log_file_name)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    return logger


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
