import time
import random
from dataclasses import asdict
import json
import datetime
import requests
from bs4 import BeautifulSoup, Tag
from item import Item

user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; rv:40.0) Gecko/20100101 Firefox/40.0",
    "Mozilla/5.0 (Windows NT 5.1; rv:22.0) Gecko/20100101 Firefox/22.0",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36 Edge/15.15063",
    "Mozilla/5.0 (Windows NT 6.1; Trident/7.0; AS; en-US) like Gecko",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36 Edge/79.0.309.65",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:35.0) Gecko/20100101 Firefox/35.0",
]
urls_to_scrape = [
    "https://www.czone.com.pk/memory-module-ram-pakistan-ppt.127.aspx?recs=20",
    "https://www.czone.com.pk/power-supply-pakistan-ppt.183.aspx?recs=20",
    "https://www.czone.com.pk/solid-state-drives-ssd-pakistan-ppt.263.aspx?recs=20",
]


def main():
    # 1. Loop over all the urls
    for url in urls_to_scrape:
        response = make_request(url)
        item_page_soup = BeautifulSoup(response.content, "html.parser")

        # 2. Scrape items links from the items pages
        items_links = scrape_items_links(item_page_soup)

        # 3. Loop over all the items links & scrape the
        # individual item data
        scraped_items = []
        for link in items_links:
            delay()  # Sleeps for some random seconds
            response2 = make_request(link)
            item_soup = BeautifulSoup(response2.content, "html.parser")
            item = scrape_item_data(item_soup)
            scraped_items.append(item)

        # Save items in json
        write_json_file(scraped_items)


# ua --> User Agent
def get_random_ua():
    random_num = random.randint(0, len(user_agents) - 1)
    random_user_agent = user_agents[random_num]
    return random_user_agent


def make_request(url):
    print("--- Making request ---")
    print("URL: ", url)
    response = requests.get(url, headers={"User-Agent": get_random_ua()}, timeout=3)
    return response


def scrape_items_links(soup):
    print("--- Scraping item links ---")
    items_urls = []

    # Get a list of items html from the items page
    items = soup.find_all("div", class_="product")

    # If there are no items to scrape, end the process
    if len(items) < 1:
        return items_urls

    for i in items:
        url = i.find("div", class_="image").a["href"]
        items_urls.append("https://www.czone.com.pk" + url)

    return items_urls


def scrape_item_data(soup):
    print("--- Scraping item data ---")
    title = soup.find(id="spnProductName").get_text() or ""
    brand = soup.find(id="spnBrand").get_text() or ""
    desc = soup.find(id="divProductDesc").get_text() or ""
    price = soup.find(id="spnCurrentPrice").get_text() or ""
    stock_status = soup.find(id="spnStockStatus").get_text() or "Not in Stock"
    ratings = 0

    # Scrape specifications from specs div
    specs_div = list(soup.find(id="producttabs1_divContent").children)
    specs = [s.get_text().strip() for s in specs_div]

    # Scrape images links from thumbnails
    images_tags = list(soup.find(id="divThumbs").children) or []
    images = []
    for img in images_tags:
        if isinstance(img, Tag):
            images.append(img["href"])

    # Scrape category from breadcrumb
    breadcrumbs = list(soup.find("ul", class_="breadcrumb").children)
    category = breadcrumbs[3].get_text().strip()

    item = Item(
        title=title,
        desc=desc,
        price=price,
        brand=brand,
        category=category,
        images=images,
        specs=specs,
        stock_status=stock_status,
        ratings=ratings,
    )
    return item


def delay():
    timer = random.randint(2, 6)
    print(f"--- Sleeping for {timer} seconds ---")
    time.sleep(timer)  # Adds a random delay


def write_json_file(items):
    print("--- Writing to file ---")
    # Use current time as the filename
    current_time = datetime.datetime.now()
    filename = "data-" + current_time.strftime("%H-%M-%S") + ".json"
    with open(filename, "w", encoding="utf-8") as file:
        json.dump([asdict(i) for i in items], file, indent=4)


main()
