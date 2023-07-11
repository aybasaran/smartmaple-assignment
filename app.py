import os
from configparser import ConfigParser

from db.mongo import save_book
from scraper.kitap_yurdu import *
from utils.helpers import build_url_with_params

# root directory
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

constants = ConfigParser()
constants.read(os.path.join(ROOT_DIR, "constants.ini"))


if __name__ == "__main__":
    KY_URL = constants["CONSTANTS"]["KY_URL"]

    book_elements, page_count = ky_scrape_books_from_page(KY_URL)
    books = ky_extract_books_from_elements(book_elements)

    for book in books:
        save_book(book, "kitapyurdu")
        break

    # print("Starting to scrape other pages...")
    # for page in range(2, page_count + 1):
    #     params = {"page": [page]}
    #     NEW_URL = build_url_with_params(KY_URL, params)
    #     print("Scraping page {}...".format(page))
    #     print("URL: {}".format(NEW_URL))

    #     # extract book fields from book element

    #     break
