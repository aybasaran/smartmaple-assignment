import os
from configparser import ConfigParser

from db.mongo import save_book
from scraper.kitap_yurdu import *
from utils.helpers import build_url_with_params, get_latest_state, set_latest_state

# root directory
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

constants = ConfigParser()
constants.read(os.path.join(ROOT_DIR, "constants.ini"))


if __name__ == "__main__":
    KY_URL = constants["CONSTANTS"]["KY_URL"]
    CURRENT_PAGE, CURRENT_PAGE_COUNT = get_latest_state()

    print("Current page: {}".format(CURRENT_PAGE))
    print("Current page count: {}".format(CURRENT_PAGE_COUNT))

    if CURRENT_PAGE == 0 and CURRENT_PAGE_COUNT == 0:
        print("Scraping page 1...")
        book_elements, page_count = ky_scrape_books_from_page(KY_URL)
        books = ky_extract_books_from_elements(book_elements)

        for book in books:
            save_book(book, "kitapyurdu")

        CURRENT_PAGE = 1
        CURRENT_PAGE_COUNT = page_count
        set_latest_state(CURRENT_PAGE, CURRENT_PAGE_COUNT)
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
            set_latest_state(CURRENT_PAGE, CURRENT_PAGE_COUNT)

        print("Scraping completed.")
