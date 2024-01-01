# Savings Tracker

Savings Tracker is a powerful tool that helps you monitor and receive timely updates on product prices from various e-commerce websites. Stay informed about price drops and take advantage of the best deals effortlessly.


## Features

- Multi-Site Tracking: Monitor prices across popular e-commerce websites through web scrapping, including AliExpress, eBay, Jiji, and Jumia.

- Automatic Updates: Receive automatic updates on price changes for your tracked products.

- Cheapest Product Finder: Find the overall cheapest product among multiple sources for your desired items.

- Background Task Scheduler: Schedule daily price checks for your favorite products at 8 AM.


## Setting Up Locally

Follow these steps to get started with Savings Tracker:

1. Installation: Install the required dependencies using the provided `requirements.txt` file.

    ```bash
    pip install -r requirements.txt
    ```
2. A MongoDB Atlas: Follow https://account.mongodb.com/account/register/ to create a MongoDB account if you don't have one, and then create a project and obtain a username, password, and a connection string.

3. Create a .env file and add the following variables

```
MONGO_URL = DB_URL_FROM_MONGODB
PORT=8000

TWILO_ACCOUNT_SID = TWILLO_ACCOUNT_SID_FROM_TWILIO
TWILO_AUTH_TOKEN = TWILLO_AUTH_TOKEN_FROM_TWILIO
TWILO_FROM_NUMBER = TWILIO_FROM_NUMBER
TWILO_TO_NUMBER = YOUR_PHONE_NUMBER
```

4. Run the Fastapi App: Spin the Fastapi server.

    ```bash
    uvicorn main:app --reload
    ```

5. Scheduled Task Trigger: To manually trigger the scheduled task, use the following command in a fresh cmd/terminal console pointing to the project's root directory:

    ```bash
    python cronjob.py
    ```


## Usage

- Track Products: Add your desired products to the list for automated price tracking.

- Receive Alerts: Receive SMS alerts for price drops and product updates.

- Update Prices: Click on provided links in SMS alerts to update prices in your database directly from your phone.


## Contributing

If you find any issues or have suggestions for improvement, feel free to open an issue or submit a pull request.


---

Happy Shopping with PriceTracker Pro!
