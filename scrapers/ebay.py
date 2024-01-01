from fastapi import HTTPException, status
import requests
from bs4 import BeautifulSoup
import re


def scrape_products(product_name: str):
    try:
        base_url = "https://www.ebay.com"
        query_url = f"{base_url}/sch/i.html?_from=R40&_trksid=p2334524.m570.l1313&_nkw=\"{product_name.replace(' ', '+')}\""
        response = requests.get(query_url)
        
        response.raise_for_status()
        
        soap = BeautifulSoup(response.text, 'html.parser')

        not_found = soap.select_one('.srp-save-null-search__heading')
        if not_found:
            return not_found.text.strip()
        
        cards = soap.find_all('div', class_="s-item__wrapper clearfix")

        data = []
        
        for card in cards:
            entry = {
                'absolute_name': product_name,
                'name': card.find('span', role="heading").get_text(strip=True),
                'description': '',
                'price': card.find('span', class_="s-item__price").get_text(strip=True),
                'image': card.find('img').get('src'),
                'link': card.find("a").get('href')
            }

            data.append(entry)

        data.pop(0)
        
        return data
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail={'msg': 'Server Error!'})


def extract_price(price_str: str) -> float:
    pattern = re.compile(r'\$([\d.]+)to\$([\d.]+)')
    
    match = pattern.match(price_str)

    if match:
        value1 = float(match.group(1).replace(',', ''))
        value2 = float(match.group(2).replace(',', ''))
        average_price = (value1 + value2) / 2
        return average_price
    else:
        return float(price_str.strip('$').replace(',', ''))
    

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
