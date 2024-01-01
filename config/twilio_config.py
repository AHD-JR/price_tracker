from twilio.rest import Client
import os
from dotenv import load_dotenv
import asyncio
import aiohttp

load_dotenv()

SID = os.environ.get('TWILIO_ACCOUNT_SID')
TOKEN = os.environ.get('TWILIO_AUTH_TOKEN')
PHONE_NUMBER = os.environ.get('TWILIO_PHONE_NUMBER')

client = Client(SID, TOKEN)

async def send_sms_async(to, message):
    try:
        async with aiohttp.ClientSession() as session:
            message = await asyncio.to_thread(
                lambda: client.messages.create(
                    body=message,
                    from_=PHONE_NUMBER,
                    to=to
                )
            )
            return message.sid
    except Exception as e:
        print(e)
        return str(e)