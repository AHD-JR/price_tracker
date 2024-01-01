import motor.motor_asyncio
import os 
from dotenv import load_dotenv

load_dotenv()

DB_URL = os.getenv('MONGO_URL')

client = motor.motor_asyncio.AsyncIOMotorClient(DB_URL)
db = client['priceupdate']

