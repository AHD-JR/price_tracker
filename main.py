from fastapi import FastAPI, HTTPException, status
from productModel import Product
from config.db import db, client
import os
from dotenv import load_dotenv
from config.twilio_config import send_sms_async
import re
import json
from urllib.parse import urlencode

load_dotenv()

app = FastAPI()

port = os.environ.get("PORT", 8000)

products_collection = db['products']

recipient_number = os.environ.get('RECIPIENT_NUMBER')

try:
    client.server_info()
    print("Connected to MongoDB 🚀")
except:
    print('Could not connect to MongoDB!')
    

@app.get('/')
async def price_update():
    return {"msg": f"Up and running on port {port}"}


def price_extraction_logic(price_string: str) -> float:
    if price_string.startswith('$'):
        price = float(re.sub(r'[^0-9.]', '', price_string)) * 1200
    else:
        price = float(re.sub(r'[^0-9.]', '', price_string))

    return price


def generate_update_link(absolute_name: str, product_dict: dict) -> str:
    try:
        base_url = "http://localhost:8000/update_product"
        path = f"/{absolute_name}"
        params = {'product_dict': json.dumps(product_dict)}
        link = f"{base_url}{path}?{urlencode(params)}"
        return link
    except Exception as e:
        print(str(e))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)) 


@app.post('/check_discount')
async def compare_and_notify(req: Product):
    try:
        product_data = req.dict()
        absolute_name = product_data.get('absolute_name')
        product = await products_collection.find_one({'absolute_name': absolute_name})
        if not product:
            products_collection.insert_one(product_data)
            return 

        old_price = price_extraction_logic(product['price'])
        new_price = price_extraction_logic(product_data.get('price'))

        if old_price > new_price:
            update_db_link = generate_update_link(absolute_name, product_data)
            
            message = f"Price update for {absolute_name} with ₦{old_price - new_price} discount." \
            f"\n View details via: {product_data.get('link')}.\n\n\nClick this link to update product: " \
            f"{update_db_link}"

            await send_sms_async(recipient_number, message)

        return 
    except Exception as e:
        print(str(e))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@app.put('/update_product/{absolute_name}')
async def update_product_in_db(absolute_name: str, req: Product):
    try:
        product = await products_collection.find_one({'absolute_name': absolute_name})
        if not product:
            return {"msg": f"Product with name '{absolute_name}' not found!"}
        
        updated_product = await products_collection.update_one({'absolute_name': absolute_name}, {'$set': req.dict()})
        if updated_product.modified_count == 0:
            return "Product not updated"
        
        return f"Product with name '{absolute_name}' is updated!"
    except Exception as e:
        print(str(e))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    

@app.delete('/delete_product/{absolute_name}')
async def delete_product(absolute_name: str):
    try:
        product = await products_collection.find_one({'absolute_name': absolute_name})
        if not product:
            return {"msg": f"Product with name '{absolute_name}' not found!"}
        
        await products_collection.delete_one({'absolute_name': absolute_name})
        
        return f"Product with name '{absolute_name}' is deleted!"
    except Exception as e:
        print(str(e))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))