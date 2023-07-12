from scraper.kitap_sepeti import ks_start_scraping
from scraper.kitap_yurdu import ky_start_scraping

if __name__ == "__main__":
    response = input("Which site do you want to scrape? (Kitapyurdu or Kiyapsepeti) (ky/ks): ")
    if response.lower() == "ky" or response == "kitapyurdu":
        ky_start_scraping()
    elif response.lower() == "ks" or response == "kiyapsepeti":
        ks_start_scraping()
