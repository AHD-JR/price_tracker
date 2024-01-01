from fastapi import HTTPException, status
import requests
from bs4 import BeautifulSoup
import re

def scrape_products(product_name: str):
    try:
        base_url = "https://www.aliexpress.com"
        query_url = f"{base_url}/w/wholesale-\"{product_name.replace(' ', '-')}\".html"
        response = requests.get(query_url)

        response.raise_for_status()
        
        soap = BeautifulSoup(response.text, 'html.parser')

        cards = soap.find_all('div', class_="list--gallery--C2f2tvm search-item-card-wrapper-gallery")

        data = []

        for card in cards:
            entry = {   
                'absolute_name': product_name,
                'name': card.find('h1', class_="multi--titleText--nXeOvyr").get_text(strip=True),
                'description': '',
                'price': card.find('div', class_="multi--price-sale--U-S0jtj").get_text(strip=True),
                'image': card.find('img').get('src') if card.find('img') else '',
                'link': card.find('a').get('href')
            }

            data.append(entry)
        
        return data  
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail={'msg': 'Server Error!'})

    

def extract_price(price_str: str) -> float:
        return float(price_str.strip('NGN').replace(',', ''))
    

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
