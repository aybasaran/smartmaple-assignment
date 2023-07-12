import re
from typing import List, Tuple

import requests
from bs4 import BeautifulSoup, PageElement

from db.mongo import save_book
from utils.helpers import get_latest_state, set_latest_state, build_url_with_params


import pathlib
import configparser
import os


ROOT_DIR = pathlib.Path(__file__).parent.parent.absolute()
constants = configparser.ConfigParser()
constants.read(os.path.join(ROOT_DIR, "constants.ini"))


def ky_scrape_books_from_page(url: str) -> Tuple[List[PageElement], int]:
    """
    Scrapes the books from the URL and returns a list of book elements.

    Returns:
        list: A list of book elements.
        page_count: The number of pages.
    """
    page = requests.get(url)

    if page.status_code != 200:
        raise Exception("Couldn't get the page. Status code: {}".format(page.status_code))

    soup = BeautifulSoup(page.content, "html.parser")
    book_elements = soup.find_all("div", class_="product-cr")
    page_count_text = soup.find("div", class_="pagination").find("div", class_="results").text

    if len(book_elements) == 0:
        raise Exception("Couldn't find any book elements.")

    # clean page request and soup
    page.close()
    soup.decompose()

    return book_elements, KY_GET_PAGE_COUNT(page_count_text)


def KY_GET_PAGE_COUNT(page_count_text) -> int:
    """
    Extracts the page count from the given page count text.

    Args:
        page_count_text (str): The page count text.

    Returns:
        int: The page count.

    """

    page = re.search(r"\((.*?)\)", page_count_text).group(1)
    page_count = int(page.split(" ")[0])
    return page_count


def ky_extract_books_from_elements(book_elements: List[PageElement]) -> List[dict]:
    """
    Extracts the books from the given book elements.

    Args:
        book_elements (list): A list of book elements.

    Returns:
        list: A list of books.
    """
    books = []

    for book_element in book_elements:
        book = {}
        title = book_element.find("div", class_="name").find("a")["title"]
        publisher = book_element.find("div", class_="publisher").find("a").find("span").text
        author_el = book_element.find("div", class_=["author", "compact"]).find("a")

        # There are some books without author
        if author_el:
            author = author_el.text
        else:
            author = "N/A"

        # on the website, the price element has two different classes
        # price-new and price-old
        # a little bit debugging i figured out that the price-new element can be null
        price_el = book_element.find("div", class_="price")
        # Even if in stock parameter is true, the price element still can be null
        if price_el:
            price_el_new = price_el.find("div", class_="price-new")
            price_el_old = price_el.find("div", class_="price-old")

            if price_el_new:
                price = price_el_new.find("span", class_="value").text
            elif price_el_old:
                price = price_el_old.find("span", class_="value").text
            else:
                price_span_el = price_el.find("span", class_="price-new")
                if not price_span_el:
                    price_span_el = price_el.find("span", class_="price-old")
                price = price_span_el.find("span", class_="value").text
        else:
            price = "N/A"

        book["title"] = title.strip()
        book["publisher"] = publisher.strip()
        book["author"] = author.strip()
        book["price"] = price.strip()
        books.append(book)

    return books


def ky_start_scraping():
    KY_URL = constants["CONSTANTS"]["KY_URL"]
    CURRENT_PAGE, CURRENT_PAGE_COUNT = get_latest_state("ky_")

    print("Current page: {}".format(CURRENT_PAGE))
    print("Current page count: {}".format(CURRENT_PAGE_COUNT))

    while CURRENT_PAGE <= CURRENT_PAGE_COUNT:
        if CURRENT_PAGE == 0 and CURRENT_PAGE_COUNT == 0:
            print("Scraping page 1...")
            book_elements, page_count = ky_scrape_books_from_page(KY_URL)
            books = ky_extract_books_from_elements(book_elements)

            for book in books:
                save_book(book, "kitapyurdu")

            CURRENT_PAGE = 1
            CURRENT_PAGE_COUNT = page_count
            set_latest_state("ky_", CURRENT_PAGE, CURRENT_PAGE_COUNT)
        else:
            for page in range(CURRENT_PAGE, CURRENT_PAGE_COUNT + 1):
                params = {"page": [page]}
                new_page_url = build_url_with_params(KY_URL, params)
                print("Scraping page {}...".format(page))
                print("URL: {}".format(new_page_url))
                book_elements, _ = ky_scrape_books_from_page(new_page_url)
                books = ky_extract_books_from_elements(book_elements)

                for book in books:
                    save_book(book, "kitapyurdu")

                CURRENT_PAGE = page
                set_latest_state("ky_", CURRENT_PAGE, CURRENT_PAGE_COUNT)

            print("Scraping completed.")
