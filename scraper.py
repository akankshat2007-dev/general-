import argparse
import csv
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

BASE_URL = "https://mdcomputers.in/"

def scrape_products(search_term):
    params = {
        "route": "product/search",
        "search": search_term
    }

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(
        BASE_URL,
        params=params,
        headers=headers,
        timeout=15
    )
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    products = []

    for product in soup.select(".product-thumb"):
        name_tag = product.select_one(".caption h4 a")
        price_tag = product.select_one(".price")

        if not name_tag:
            continue

        name = name_tag.get_text(" ", strip=True)
        url = urljoin(BASE_URL, name_tag.get("href", ""))

        price = price_tag.get_text(" ", strip=True) if price_tag else "N/A"

        products.append({
            "name": name,
            "price": price,
            "url": url
        })

    return products


def save_csv(products, filename="products.csv"):
    with open(filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=["name", "price", "url"]
        )
        writer.writeheader()
        writer.writerows(products)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Scrape product details from MDComputers"
    )
    parser.add_argument(
        "search",
        nargs="+",
        help="Product search term"
    )

    args = parser.parse_args()
    search_term = " ".join(args.search)

    products = scrape_products(search_term)

    print(f"Found {len(products)} products:\n")

    for product in products:
        print(f"Product: {product['name']}")
        print(f"Price: {product['price']}")
        print(f"URL: {product['url']}")
        print("-" * 60)

    save_csv(products)
    print("\nResults saved to products.csv")
