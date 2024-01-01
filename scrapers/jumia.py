from fastapi import HTTPException, status
import requests
from requests.exceptions import RequestException
from bs4 import BeautifulSoup
import re

def scrape_products(product_name: str):
    try:
        base_url = "https://www.jumia.com.ng"
        query_url = f"{base_url}/catalog/?q=\"{product_name.replace(' ', '+')}\""

        response = requests.get(query_url)

        response.raise_for_status()
        
        soap = BeautifulSoup(response.text, 'html.parser')
        
        not_found = soap.find('h2', class_="-pvs -fs16 -m")

        if not_found:
            return not_found.get_text(strip=True)
        
        cards = soap.find_all('a', class_="core")

        data = []

        for card in cards:
            entry = {
                'absolute_name': product_name,
                'name': card.find('h3', class_="name").get_text(strip=True),
                'description': '',
                'price': card.find('div', class_="prc").get_text(strip=True),
                'image': card.find('img').get('data-src'),
                'link': f"{base_url}{card.get('href')}"
            }

            data.append(entry)
        
        return data
        
    except RequestException as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail={'msg': f'Request Error: {e}'})
    
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail={'msg': 'Server Error!'})
    

def extract_price(price_str: str) -> float:
    pattern = re.compile(r'₦\s*([\d,]+)\s*-\s*₦\s*([\d,]+)')
    
    match = pattern.match(price_str)

    if match:
        value1 = float(match.group(1).replace(',', ''))
        value2 = float(match.group(2).replace(',', ''))
        average_price = (value1 + value2) / 2
        return average_price
    else:
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

