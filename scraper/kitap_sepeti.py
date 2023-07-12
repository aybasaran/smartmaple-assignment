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


def ks_scrape_books_from_page(url: str) -> Tuple[List[PageElement], int]:
    """
    Scrapes the books from the URL and returns a list of book elements.

    Returns:
        list: A list of book elements.
        page_count: The number of pages.
    """

    print("Scraping page: {}".format(url))

    page = requests.get(url)

    if page.status_code != 200:
        raise Exception("Couldn't get the page. Status code: {}".format(page.status_code))

    soup = BeautifulSoup(page.content, "html.parser")
    book_elements = soup.find_all("div", class_="productItem")
    pagination_el = soup.find("div", class_="productPager")

    page_numbers_el = pagination_el.find_all("a")
    page_count_text = page_numbers_el[-2].text

    if len(book_elements) == 0:
        raise Exception("Couldn't find any book elements.")

    if not page_count_text:
        raise Exception("Couldn't find any page count.")

    page.close()
    soup.decompose()

    return book_elements, int(page_count_text)


def ks_extract_books_from_elements(book_elements: List[PageElement]) -> List[dict]:
    """
    Extracts the books from the given book elements.

    Args:
        book_elements (list): The book elements.

    Returns:
        list: A list of books.
    """

    books = []

    for book_element in book_elements:
        book = {}
        details_el = book_element.find("div", class_="productDetails")
        details = details_el.find_all("a")
        title = details[0].text.strip()
        publisher = details[1].text.strip()
        author = details[2].text.strip()
        price = (
            details_el.find("div", class_="productPrice").find("div", class_="currentPrice").text.strip().split("\n")[0]
        )
        book["title"] = title
        book["publisher"] = publisher
        book["author"] = author
        book["price"] = price
        books.append(book)

    return books


def ks_start_scraping():
    KS_URL = constants["CONSTANTS"]["KS_URL"]
    CURRENT_PAGE, CURRENT_PAGE_COUNT = get_latest_state("ks_")

    print("Current page: {}".format(CURRENT_PAGE))
    print("Current page count: {}".format(CURRENT_PAGE_COUNT))

    while CURRENT_PAGE <= CURRENT_PAGE_COUNT:
        if CURRENT_PAGE == 0 and CURRENT_PAGE_COUNT == 0:
            print("Scraping page 1...")
            book_elements, page_count = ks_scrape_books_from_page(KS_URL)
            books = ks_extract_books_from_elements(book_elements)

            for book in books:
                save_book(book, "kitapsepeti")

            CURRENT_PAGE = 1
            CURRENT_PAGE_COUNT = page_count
            set_latest_state("ks_", CURRENT_PAGE, CURRENT_PAGE_COUNT)
        else:
            for page in range(CURRENT_PAGE, CURRENT_PAGE_COUNT + 1):
                params = {"pg": [page]}
                new_page_url = build_url_with_params(KS_URL, params)
                print("Scraping page {}...".format(page))
                print("URL: {}".format(new_page_url))
                book_elements, _ = ks_scrape_books_from_page(new_page_url)
                books = ks_extract_books_from_elements(book_elements)

                for book in books:
                    save_book(book, "kitapsepeti")

                CURRENT_PAGE = page
                set_latest_state("ks_", CURRENT_PAGE, CURRENT_PAGE_COUNT)

        print("Scraping completed.")
