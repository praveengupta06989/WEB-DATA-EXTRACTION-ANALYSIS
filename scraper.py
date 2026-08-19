"""
TASK 5 - WEB DATA EXTRACTION & ANALYSIS
Scrapes the public Books to Scrape educational website.

Run directly:
    python scraper.py

Or run the whole project:
    python main.py
"""

from pathlib import Path
import time
import requests
from bs4 import BeautifulSoup
import pandas as pd

PROJECT_DIR = Path(__file__).resolve().parent
DATA_DIR = PROJECT_DIR / "data"
RAW_FILE = DATA_DIR / "raw_books.csv"

BASE_URL = "https://books.toscrape.com/"
START_URL = BASE_URL + "catalogue/page-1.html"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Educational Web Data Extraction Project)"
}

RATING_MAP = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}


def rating_to_number(classes):
    for item in classes:
        if item in RATING_MAP:
            return RATING_MAP[item]
    return None


def scrape_page(url):
    response = requests.get(url, headers=HEADERS, timeout=20)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    records = []

    for product in soup.select("article.product_pod"):
        title_tag = product.select_one("h3 a")
        price_tag = product.select_one(".price_color")
        rating_tag = product.select_one("p.star-rating")
        availability_tag = product.select_one(".availability")

        if title_tag is None:
            continue

        relative_url = title_tag.get("href", "")
        product_url = requests.compat.urljoin(url, relative_url)

        rating = rating_to_number(
            rating_tag.get("class", []) if rating_tag else []
        )

        availability = (
            availability_tag.get_text(" ", strip=True)
            if availability_tag else ""
        )

        price = (
            price_tag.get_text(strip=True).replace("£", "").strip()
            if price_tag else ""
        )

        records.append({
            "title": title_tag.get("title", title_tag.get_text(strip=True)),
            "price_gbp": price,
            "rating": rating,
            "availability": availability,
            "product_url": product_url,
        })

    next_tag = soup.select_one("li.next a")
    next_url = (
        requests.compat.urljoin(url, next_tag.get("href"))
        if next_tag else None
    )

    return records, next_url


def scrape_all_pages():
    records = []
    url = START_URL
    page_number = 0

    while url:
        page_number += 1
        print(f"Scraping page {page_number}...")

        page_records, url = scrape_page(url)
        records.extend(page_records)

        time.sleep(0.5)

    return pd.DataFrame(records)


def main():
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    try:
        df = scrape_all_pages()

        if df.empty:
            raise RuntimeError("No products were collected from the website.")

        df.to_csv(RAW_FILE, index=False, encoding="utf-8-sig")

        print()
        print(f"SUCCESS: {len(df)} products collected.")
        print(f"Saved to: {RAW_FILE}")

    except requests.RequestException as error:
        print("ERROR: Could not access the website.")
        print(f"Details: {error}")
        raise SystemExit(1)

    except Exception as error:
        print(f"ERROR: {error}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
