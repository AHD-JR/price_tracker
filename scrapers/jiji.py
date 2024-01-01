from fastapi import HTTPException, status
import requests
from bs4 import BeautifulSoup


def scrape_products(product_name: str):
    try:
        base_url = "https://jiji.ng"
        query_url = f"{base_url}/search?query=\"{product_name.replace(' ', '%')}\""

        response = requests.get(query_url)
        
        response.raise_for_status()
        
        soap = BeautifulSoup(response.text, 'html.parser')

        not_found = soap.find('div', class_="b-adverts-listing__extra-title h-mt-15 h-mb-5 qa-listing-no-results")
        
        if not_found:
            return not_found.text.strip()

        cards = soap.find_all('div', class_="b-list-advert__gallery__item js-advert-list-item")

        data = []

        for card in cards:
            entry = {
                'absolute_name': product_name,
                'name': card.find('div', class_="b-advert-title-inner qa-advert-title b-advert-title-inner--div").get_text(strip=True),
                'description': card.find('div', class_="b-list-advert-base__description-text").get_text(strip=True),
                'price': card.find('div', class_="qa-advert-price").get_text(strip=True),
                'image': card.find('img').get('src'),
                'link': f"{base_url}{card.find('a').get('href')}"
            }

            data.append(entry)

        return data   
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail={'msg': 'Server Error!'})


def extract_price(price_str: str) -> float:
        return float(price_str.strip('₦').replace(',', ''))
   

def get_cheapest_product(data: list):
    try:
        if not isinstance(data, list):
            return data
        
        chippest_product: dict = data[0]

        for product_data in data:
            if extract_price(product_data["price"]) < extract_price(chippest_product["price"]):
                chippest_product = product_data
        
        return chippest_product
    except Exception as e:
        return str(e)
