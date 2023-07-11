import re
from typing import List, Tuple

import requests
from bs4 import BeautifulSoup, PageElement


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

    return book_elements, KY_GET_PAGE_COUNT(page_count_text)


def KY_GET_PAGE_COUNT(page_count_text) -> int:
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

        # extract book fields from book element

        title = book_element.find("div", class_="name").find("a")["title"]
        publisher = book_element.find("div", class_="publisher").find("a").find("span").text
        author = book_element.find("div", class_=["author", "compact"]).find("a").text
        price = (
            book_element.find("div", class_="price").find("div", class_="price-new").find("span", class_="value").text
        )

        book["title"] = title.strip()
        book["publisher"] = publisher.strip()
        book["author"] = author.strip()
        # convert price to float
        book["price"] = float(price.strip().replace(",", "."))
        books.append(book)

    return books