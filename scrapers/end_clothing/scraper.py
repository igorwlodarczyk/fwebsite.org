from scrapers.end_clothing import constants as const
from datetime import datetime
from playwright.sync_api import sync_playwright
from common.utils import clear_debug_logs, parse_price, get_logger
from common.constants import user_agent
from bs4 import BeautifulSoup


def get_data(url: str) -> tuple:
    """
    Retrieves price and available sizes for a product from a given URL.

    :param url: The URL of the product page.
    :return: A tuple containing the parsed price, parsed sizes, current date, and currency.
    :rtype: tuple
    """
    with sync_playwright() as p:
        logger = get_logger("End_clothing")
        logger.debug(f"Start url: {url}")
        try:
            currency = const.currency
            browser = p.chromium.launch(headless=False)
            context = browser.new_context()
            context.set_extra_http_headers({"User-Agent": user_agent})
            page = context.new_page()
            page.goto(url)
            logger.debug("Trying to get the price...")
            page.wait_for_selector(const.xpath_price, timeout=const.timeout)
            price = page.locator(const.xpath_price).text_content()
            logger.debug("Successfully gotten price!")
            logger.debug("Trying to get available sizes...")
            sizes_element_html = page.inner_html(const.css_sizes)
            soup = BeautifulSoup(sizes_element_html, "html.parser")
            sizes = soup.find_all("div", class_=lambda x: x and x.startswith("sc"))
            parsed_sizes = [size.text for size in sizes]
            logger.debug("Successfully gotten available sizes!")
            parsed_price = parse_price(price)
            date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            return parsed_price, parsed_sizes, date, currency
        except Exception as e:
            logger.error(f"Error occurred: {str(e)}", exc_info=True)
        finally:
            clear_debug_logs()
