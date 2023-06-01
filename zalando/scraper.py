import logging
import uuid
import zalando.constants as const
from datetime import datetime
from playwright.sync_api import sync_playwright
from common.utils import clear_debug_logs, parse_price
from zalando.utils import parse_sizes, get_currency


def get_data(url: str) -> tuple:
    """
    Retrieves data (price, sizes, date, and currency) from a given URL of a product page.

    :param url: The URL of the product page from which to retrieve data.
    :return: A tuple containing the parsed price, parsed sizes, date, and currency.

    The function performs the following steps:
    1. Initializes logging for scraping information.
    2. Retrieves the currency associated with the provided URL.
    3. Launches a Chromium browser and creates a new browsing context.
    4. Sets the User-Agent header for the HTTP requests to mimic a specific user agent.
    5. Navigates to the provided URL.
    6. Accepts cookies if a cookies button is present on the page.
    7. Retrieves the price of the product, either the discounted price or the regular price.
    8. Retrieves the available sizes of the product.
    9. If the product is indicated as a one-size item, retrieves that information instead.
    10. Parses the price and sizes to remove any unwanted characters or formatting.
    11. Returns a tuple containing the parsed price, parsed sizes, current date and time, and currency.

    Note:
    - If an error occurs during the process, it is logged with the associated exception details.
    - Debug logs are cleared after the data retrieval process.
    """
    with sync_playwright() as p:
        unique_id = str(uuid.uuid4())[:10]
        logger = logging.getLogger(f"Zalando_scraper__{unique_id}")
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
        logger.debug(f"Start url: {url}")
        try:
            currency = get_currency(url)
            browser = p.chromium.launch(headless=False)
            context = browser.new_context()
            context.set_extra_http_headers({"User-Agent": const.user_agent})
            page = context.new_page()
            page.goto(url)
            logger.debug("Trying to accept cookies...")
            try:
                page.wait_for_selector(
                    const.xpath_cookies_button, timeout=const.timeout
                )
                page.locator(const.xpath_cookies_button).click()
                logger.debug("Successfully accepted cookies")
            finally:
                try:
                    logger.debug("Trying to get discounted price...")
                    page.wait_for_selector(
                        const.xpath_discounted_price, timeout=const.timeout
                    )
                    price = page.locator(const.xpath_discounted_price).text_content()
                    logger.debug("Successfully gotten discounted price!")
                except:
                    logger.debug("Trying to get regular price...")
                    page.wait_for_selector(
                        const.xpath_regular_price, timeout=const.timeout
                    )
                    price = page.locator(const.xpath_regular_price).text_content()
                    logger.debug("Successfully gotten regular price!")
                finally:
                    logger.debug(f"Scraped price: {price}")
                    try:
                        logger.debug("Trying to get available sizes...")
                        page.wait_for_selector(
                            const.xpath_sizes_button, timeout=const.timeout
                        )
                        page.locator(const.xpath_sizes_button).click()
                        page.wait_for_selector(const.xpath_sizes, timeout=const.timeout)
                        sizes = page.locator(const.xpath_sizes).all_inner_texts()
                        logger.debug("Successfully gotten available sizes!")
                    except:
                        logger.debug("Checking if this item is one size")
                        page.wait_for_selector(
                            const.css_one_size, timeout=const.timeout
                        )
                        sizes = page.locator(const.css_one_size).text_content()
                        logger.debug("It is one size item")
                    finally:
                        parsed_price = parse_price(price)
                        parsed_sizes = parse_sizes(sizes)
                        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        return parsed_price, parsed_sizes, date, currency
        except Exception as e:
            logger.error(f"Error occurred: {str(e)}", exc_info=True)
        finally:
            clear_debug_logs()
