# amazon_item_tracker.py

# NOTE: 
# 'a_price' and 'd_price' respectively refers to 'actual price' and 'desired price'.
# The latter refers to the price the user wishes the item to be. Whereas the former
# refers to the 'actual' price scraped from their respective amazon webpage.


import re
import time
import requests
import email_component
from program_help import ait_help
from registry import Registry
from typing import List
from typing import Dict
from typing import Tuple
from bs4 import BeautifulSoup as BS


INTERVAL = 3600
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36"}
REG = Registry()


def main_menu_text() -> None:
    print('_____________________')
    print('[AMAZON ITEM TRACKER]')
    print('[Enter 1, 2, or 3...]')
    print('_____________________')
    print('1 -> Ping Prices')
    print('2 -> Configure')
    print('3 -> Monitor Prices [Email]')
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

    if(actual.lower()=='price not found'):
        return False
    return True if(parse_price(actual) < float(desired)) else False


def url_to_soup_obj(url: str) -> BS:
    try:
        page = requests.get(link, headers=HEADERS)
    except requests.exceptions.MissingSchema:
        print(f"\n[WARINING] - <link: {link}> - INVALID!")
        print("LINK DOES NOT CONTAIN PROTOCOL i.e 'https://'")
        return 
    return BS(page.content, 'html5lib')


def analyze_non_book(soup: BS) -> Tuple[str, str]:
    item_name = soup.find("span", id="productTitle").get_text().strip()
    item_a_price = soup.find("span", id="price_inside_buybox").get_text().strip()
    return (item_name, item_a_price)


def seek_kindle_price(soup: BS) -> str:
    """ Locating the kindle edition price returns multiple objects in a list.
        As the price never contains letters or specific punctuation.
        Using regular expression whose object is the actual price is returned.
    """
 
    kindle_arr = soup.find_all("span", class_="a-size-base a-color-secondary")
    for soup_obj in kindle_arr:
        string = soup_obj.get_text()
        if(len(re.findall("[+*|(){}%!]", string)) > 0 or len(re.findall("[a-z]", string)) > 0):
            continue
        else:
            return string.strip()
    return "Price Not Found"


def seek_paperback_price(soup: BS) -> str:
    try:
        return soup.find("span", class_="a-size-base a-color-price a-color-price").get_text().strip()
    except AttributeError:
        return "Price Not Found"


def analyze_book(soup: BS) -> None:
    return seek_paperback_price(soup), seek_kindle_price(soup)


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

        if(len(parts) == 2):    # NON-BOOK BRANCH
            # try-except prevents -> crashing upon webpage not containg specific <span ...>
            try:
                item_name, item_a_price = analyze_non_book(soup)
            except AttributeError:
                print(f"\n[WARNING] - <link: {link}> - INVALID!")
                print("WEBPAGE DOES NOT CONTAIN PRICE")
                continue
            yield(item_name, item_a_price, desired_price)
        else:                   # BOOK BRANCH
            pb_price, ke_price = analyze_book(soup)
            desired_pb_price, desired_ke_price = parts[1], parts[2]
            yield(soup.title.get_text(), pb_price, ke_price, desired_pb_price, desired_ke_price)
    pass


def ping_prices() -> None:
    """ returns: dictionary 'name: str' : 'a_price: float' for each item """
    
    non_books, books = {}, {}
    links = REG.load_links()[0]
    # for each specified link the item_name and a_price is extracted, printed and returned
    data = analyze_items(links)
    for loops in range(len(links)):
        # an invalid links leads to skipping an iteration which in turn raises StopIteration
        try:
            output = next(data)
        except StopIteration:
            break
        if(len(output) == 3):
            non_books.update({output[0]: output[1]})
        elif(len(output) == 5):
            books.update({output[0]: [output[1], output[2]]})
    # this is where the item name and price are printed
    for k,v in non_books.items():
        print(f"\n<NAME  -> {k}>\n<PRICE -> {v}>")
    for k,v in books.items():
        print(f"\n<NAME            -> {k}>\n<PAPERBACK PRICE -> {v[0]}>\n<KINDLE PRICE    -> {v[1]}>")
    pass


def monitor_prices() -> None:
    """ continuously compares prices approx. every 50sec and sends an email when
        the price of an item has been reduced to a specified desired price """

    email_component.instructions()
    try:
        sender_email    = email_component.set_sender_email()
        sender_email_pw = email_component.set_sender_pw()
        receiver_email  = email_component.set_receiver_email()
    except TypeError as e:
        print(e)
        return

    while True:    
        lines = REG.load_links()[0]     # [str1, str2, str3, ...] -> strX = "<URL>,<D_PRICE>"
        data = analyze_items(lines)     # rv = (name: str, a_price: float)
        results = []                    # todo: remove this to reduce memory REPLACE -> import email l0l
        for loops in range(len(lines)):
            # extract line of text from text file
            try:
                output = next(data)    
            except StopIteration:
                break
            # non-book comparison
            print()
            if(len(output)==3): 
                if(check_price(output[2], output[1])):
                    email_component.send_email(receiver_email, sender_email,
                                               sender_email_pw, {output[0]})                
            # book paperback and kindle comparison
            elif(len(output)==5):
                #print("PB good") if(check_price(output[3], output[1])) else print("PB not good")
                #print("KE good") if(check_price(output[4], output[2])) else print("KE not good")
                if(check_price(output[3], output[1])):
                    email_component.send_email(receiver_email, sender_email,
                                               sender_email_pw, {output[0]})
                if(check_price(output[4], output[1])):
                    email_component.send_email(receiver_email, sender_email,
                                               sender_email_pw, {output[0]})
        time.sleep(INTERVAL)
    pass


def main() -> None:
    options = {1: ping_prices, 2: REG.reg_menu, 3: monitor_prices, 4: ait_help}
    while True:
        # try-except prevents -> crashing upon invalid input
        try:
            main_menu_text()
            options.get(int(input("Enter choice: ")))()
        except (ValueError, TypeError):
            print("\n[Invalid option! *.*]")


if __name__ == "__main__":
    main()
