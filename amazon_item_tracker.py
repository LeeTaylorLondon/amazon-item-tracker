# amazon_item_tracker.py

# NOTE: 
# 'a_price' and 'd_price' respectively refers to 'actual price' and 'desired price'.
# The latter refers to the price the user wishes the item to be. Whereas the former
# refers to the 'actual' price scraped from their respective amazon webpage.

import requests
from registry import Registry
from typing import List
from typing import Dict
from typing import Tuple
from bs4 import BeautifulSoup as BS


HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36"}
REG = Registry()


def main_menu_text() -> None:
    print('_____________________')
    print('[AMAZON ITEM TRACKER]')
    print('[Enter 1, 2, or 3...]')
    print('_____________________')
    print('1 -> Ping Prices')
    print('2 -> Configure')
    print('3 -> Monitor Prices')
    print('4 -> Help/Guide')
    print('_____________________')
    pass


def parse_price(s: str) -> float:
    """ The calculation is two parts as represented below
        [pounds] + [pennies] -> int(...) + float(...)
        
        returns: float value representing price of item
    """
    
    m = len(s)
    return int(s[1:m-3].replace(',', '')) + float(s[m-3::])


def check_price(desired: str, actual: str) -> bool:
    """ given two prices as strings using func -> parse_price()
        the strings are converted to float values then compared
    """

    return True if(parse_price(actual) < float(desired)) else False


def analyze_items(lines: List[str]) -> Tuple[str, str, str]:
    """ extracts actual name & price of item from given URLs

        an invalid link is defined by not having a price on the webpage
        or, not starting with a protocol such as 'https'

        an invalid link calls 'continue' to skip to the next URL

        yields: (amazon_item_name: str, amazon_price: str, desired_price: str)
    """

    for line in lines:
        parts = line.split(',')  # [<url_to_item: str>, <desired_price: float>]
        link, desired_price = parts[0], parts[1]
        # try-except prevents -> crashing upon link not containing protocol
        try:
            page = requests.get(link, headers=HEADERS)
        except requests.exceptions.MissingSchema:
            print(f"\n[WARINING] - <link: {link}> - INVALID!")
            print("LINK DOES NOT CONTAIN PROTOCOL i.e 'https://'")
            continue
        soup = BS(page.content, 'html5lib')
        # try-except prevents -> crashing upon webpage not containg specific <span ...>
        try:
            item_name = soup.find("span", id="productTitle").get_text().strip()
            item_a_price = soup.find("span", id="price_inside_buybox").get_text().strip()
        except AttributeError:
            print(f"\n[WARNING] - <link: {link}> - INVALID!")
            print("WEBPAGE DOES NOT CONTAIN PRICE")
            continue
        yield(item_name, item_a_price, desired_price)
    pass


def ping_prices() -> Dict[str, float]:
    """ returns: dictionary 'name: str' : 'a_price: float' for each item """
    
    rv = {}
    links = REG.load_links()
    # for each specified link the item_name and a_price is extracted, printed and returned
    data = analyze_items(links)
    for loops in range(len(links)):
        # an invalid links leads to skipping an iteration which in turn raises StopIteration
        try:
            output = next(data)
        except StopIteration:
            break
        rv.update({output[0]: output[1]})
    # this is where the item name and price are printed
    for k,v in rv.items():
        print(f"\n<NAME  -> {k}>\n<PRICE -> {v}>")
    return rv


# TODO: when func, check_price(), returns <true>, send email to <specified email>
# TODO: convert to continuous loop which compares prices every 50 to 60 seconds
# TODO: allow user to specify time interval when to check prices
def monitor_prices() -> None:
    """ continuously compares prices approx. every 50sec and sends an email when
        the price of an item has been reduced to a specified desired price """

    lines = REG.load_links()        # [str1, str2, str3, ...] -> strX = "<URL>,<D_PRICE>"
    data = analyze_items(lines)     # rv = (name: str, a_price: float)
    results = []                    # todo: remove this to reduce memory REPLACE -> import email l0l
    
    for loops in range(len(lines)):
        try:
            output = next(data)     # output = Tuple[i_name: str, a_price: str, d_price: str]
        except StopIteration:
            break
        results.append(check_price(output[2], output[1]))
    pass


def main() -> None:
    options = {1: ping_prices, 2: REG.reg_menu, 3: monitor_prices}
    while True:
        # try-except prevents -> crashing upon invalid input
        try:
            main_menu_text()
            options.get(int(input("Enter choice: ")))()
        except (ValueError, TypeError):
            print("\n[Invalid option! *.*]")


if __name__ == "__main__":
    main()
