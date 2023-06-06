from common.utils import convert_size_uk_to_us, parse_sizes
from typing import Union


def detect_shoe_sizes_and_parse(sizes: Union[list, str]) -> list:
    """
    Detects and parses shoe sizes from various measurement systems to US measurement.

    :param sizes: The sizes to be detected and parsed. It can be either a list of strings or a single string.
    :return: The parsed sizes as a list of strings.

    If the input `sizes` is a string, it is parsed into a list of sizes using the `parse_sizes` function.
    Each size in the list is checked to determine its measurement system.
    - If a size starts with "UK ", it is considered a UK size and converted to US size using the `convert_size_uk_to_us` function.
    - Sizes from other measurement systems are left unchanged.
    The parsed sizes are stored in a new list `parsed_sizes`, which is returned as the result.
    """
    sizes = parse_sizes(sizes)
    parsed_sizes = []
    for size in sizes:
        if size.startswith("UK "):
            parsed_size = size.replace("UK ", "")
            parsed_size = str(convert_size_uk_to_us(float(parsed_size)))
            parsed_sizes.append(parsed_size)
        else:
            parsed_sizes.append(size)
    return parsed_sizes
