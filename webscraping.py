import requests
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
import csv
import json
import urllib3

urllib3.disable_warnings(
    urllib3.exceptions.InsecureRequestWarning
)


def get_soup_requests(url):

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 "
            "Chrome/120.0 Safari/537.36"
        )
    }

    response = requests.get(
        url,
        headers=headers,
        timeout=15,
        verify=False
    )

    response.raise_for_status()

    return BeautifulSoup(
        response.text,
        "html.parser"
    )


def get_soup_playwright(url):

    print("\nOpening browser using Playwright...")
    print("Waiting for JavaScript content...")

    with sync_playwright() as p:

        browser = p.chromium.launch(
            headless=True
        )

        context = browser.new_context(
            ignore_https_errors=True,
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 "
                "Chrome/120.0 Safari/537.36"
            )
        )

        page = context.new_page()

        page.goto(
            url,
            wait_until="networkidle",
            timeout=30000
        )

        html = page.content()

        browser.close()

    return BeautifulSoup(
        html,
        "html.parser"
    )


def extract_json_ld(soup):

    products = []

    scripts = soup.find_all(
        "script",
        type="application/ld+json"
    )

    for script in scripts:

        try:

            if not script.string:
                continue

            data = json.loads(
                script.string
            )

        except (
            json.JSONDecodeError,
            TypeError
        ):

            continue

        if isinstance(data, dict):

            if data.get("@type") == "Product":

                products.append(data)

            elif data.get("@type") == "ItemList":

                for item in data.get(
                    "itemListElement",
                    []
                ):

                    if isinstance(item, dict):

                        product = item.get("item")

                        if (
                            isinstance(product, dict)
                            and product.get("@type")
                            == "Product"
                        ):

                            products.append(
                                product
                            )

        elif isinstance(data, list):

            for item in data:

                if (
                    isinstance(item, dict)
                    and item.get("@type")
                    == "Product"
                ):

                    products.append(item)

    return products


def find_text(element, selectors):

    for selector in selectors:

        found = element.select_one(
            selector
        )

        if found:

            text = found.get_text(
                " ",
                strip=True
            )

            if text:

                return text

    return "N/A"


def extract_html_products(soup):

    product_selectors = [
        "article",
        "[class*='product']",
        "[class*='Product']",
        "[class*='item']",
        "[class*='Item']",
        "[data-product]",
        "[data-testid*='product']",
        "li"
    ]

    name_selectors = [
        "h1",
        "h2",
        "h3",
        "h4",
        ".product-title",
        ".product-name",
        "[class*='product-title']",
        "[class*='product-name']",
        "[class*='title']",
        "[class*='Title']",
        "[data-testid*='title']",
        "a[title]"
    ]

    price_selectors = [
        ".price",
        ".product-price",
        "[class*='price']",
        "[class*='Price']",
        "[data-price]",
        "[data-testid*='price']"
    ]

    rating_selectors = [
        ".rating",
        ".product-rating",
        "[class*='rating']",
        "[class*='Rating']",
        "[aria-label*='rating']",
        "[aria-label*='Rating']",
        "[data-rating]"
    ]

    products = []
    containers = []

    for selector in product_selectors:

        found = soup.select(selector)

        for element in found:

            if element not in containers:

                containers.append(element)

    for container in containers:

        name = find_text(
            container,
            name_selectors
        )

        price = find_text(
            container,
            price_selectors
        )

        rating = find_text(
            container,
            rating_selectors
        )

        if (
            name != "N/A"
            or price != "N/A"
        ):

            products.append({
                "name": name,
                "price": price,
                "rating": rating
            })

    return products


def convert_json_products(json_products):

    products = []

    for product in json_products:

        name = product.get(
            "name",
            "N/A"
        )

        price = "N/A"

        offers = product.get(
            "offers"
        )

        if isinstance(
            offers,
            dict
        ):

            price = offers.get(
                "price",
                offers.get(
                    "lowPrice",
                    "N/A"
                )
            )

            currency = offers.get(
                "priceCurrency"
            )

            if (
                price != "N/A"
                and currency
            ):

                price = f"{currency} {price}"

        rating = "N/A"

        aggregate_rating = product.get(
            "aggregateRating"
        )

        if isinstance(
            aggregate_rating,
            dict
        ):

            rating = aggregate_rating.get(
                "ratingValue",
                "N/A"
            )

        products.append({
            "name": str(name),
            "price": str(price),
            "rating": str(rating)
        })

    return products


def remove_duplicates(products):

    unique_products = []
    seen = set()

    for product in products:

        key = (
            product["name"],
            product["price"],
            product["rating"]
        )

        if key not in seen:

            seen.add(key)

            unique_products.append(
                product
            )

    return unique_products


def save_to_csv(products):

    with open(
        "products.csv",
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.writer(file)

        writer.writerow([
            "Product Name",
            "Price",
            "Rating"
        ])

        for product in products:

            writer.writerow([
                product["name"],
                product["price"],
                product["rating"]
            ])


def main():

    print("=" * 60)
    print("       E-COMMERCE WEB SCRAPER")
    print("=" * 60)

    url = input(
        "\nEnter the e-commerce website URL: "
    ).strip()

    if not url.startswith(
        ("http://", "https://")
    ):

        url = "https://" + url

    products = []

    print(
        "\n[1/2] Trying standard HTML scraping..."
    )

    try:

        soup = get_soup_requests(url)

        json_products = extract_json_ld(soup)

        if json_products:

            print(
                "Structured product data found."
            )

            products = convert_json_products(
                json_products
            )

        else:

            print(
                "Structured data not found."
            )

            print(
                "Searching HTML structure..."
            )

            products = extract_html_products(
                soup
            )

    except Exception as error:

        print(
            "Standard scraping failed."
        )

        print(
            "Reason:",
            error
        )

    products = remove_duplicates(products)

    if len(products) == 0:

        print(
            "\nNo products found using "
            "standard scraping."
        )

        print(
            "Switching to JavaScript-enabled scraping..."
        )

        try:

            soup = get_soup_playwright(url)

            json_products = extract_json_ld(soup)

            if json_products:

                print(
                    "Structured product data found "
                    "after JavaScript rendering."
                )

                products = convert_json_products(
                    json_products
                )

            else:

                print(
                    "Searching rendered HTML..."
                )

                products = extract_html_products(
                    soup
                )

            products = remove_duplicates(
                products
            )

        except Exception as error:

            print(
                "\nPlaywright scraping failed."
            )

            print(
                "Reason:",
                error
            )

    if products:

        save_to_csv(products)

        print(
            "\n" + "=" * 60
        )

        print(
            "SCRAPING COMPLETED SUCCESSFULLY"
        )

        print(
            "=" * 60
        )

        print(
            f"\nProducts found: {len(products)}"
        )

        print(
            "Output file: products.csv"
        )

        print(
            "\nFirst 5 results:\n"
        )

        for product in products[:5]:

            print(
                "Name   :",
                product["name"]
            )

            print(
                "Price  :",
                product["price"]
            )

            print(
                "Rating :",
                product["rating"]
            )

            print(
                "-" * 40
            )

    else:

        print(
            "\nNo products could be detected."
        )

        print(
            "\nPossible reasons:"
        )

        print(
            "1. The website uses an "
            "unsupported structure."
        )

        print(
            "2. The website requires login."
        )

        print(
            "3. The website blocks automated requests."
        )

        print(
            "4. The website uses an API "
            "instead of visible HTML."
        )


if __name__ == "__main__":
    main()