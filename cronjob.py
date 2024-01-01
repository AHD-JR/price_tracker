from fastapi import FastAPI, HTTPException, status
import requests 
import aiocron
import asyncio
from scrapers import aliexpress, ebay, jiji, jumia
import re


app = FastAPI()

product_names = ["keyboard", "earpod"]

scrappers = [aliexpress, ebay, jiji, jumia]


def get_overall_cheapest(related_products: list):
    overall_chippest_product = related_products[0]
    min_price = float(re.sub(r'[^0-9.]', '', related_products[0]['price'])) 

    for product in related_products[1:]:
        price_string: str = product['price']
        if price_string.startswith('$'):
            price = float(re.sub(r'[^0-9.]', '', price_string)) * 1200
        else:
            price = float(re.sub(r'[^0-9.]', '', price_string))

        if min_price > price:
            overall_chippest_product = product
            min_price = price
    
    return overall_chippest_product


def post_to_my_server(data: dict):
    try:
        url = "http://localhost:8000/check_discount"

        response = requests.post(url, json=data)

        response.raise_for_status()

        print("Request sent successfully!")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail={'msg': 'Server Error!'})


async def scrape_and_post(product_name: str):
    try:
        print(product_name)
        cheapest_products = []
        for scraper in scrappers:
            data = scraper.scrape_products(product_name)
            cheapest_product = scraper.get_cheapest_product(data)
            cheapest_products.append(cheapest_product)

        overall_cheapest_product = get_overall_cheapest(cheapest_products)

        post_to_my_server(overall_cheapest_product)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail={'msg': 'Server Error!'})


async def main():
    try:
        for product_name in product_names:
            await scrape_and_post(product_name)

        for product_name in product_names:
            cron = aiocron.crontab("0 8 * * *", func=lambda: asyncio.create_task(scrape_and_post(product_name)))
            await cron.next()

        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        pass
    finally:
        loop.close()