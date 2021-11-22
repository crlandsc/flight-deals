import requests

SHEETY_URL = os.environ.get("SHEETY_URL")
SHEETY_USERS_URL = os.environ.get("SHEETY_USERS_URL")
SHEETY_AUTH = os.environ.get("SHEETY_AUTH")

class DataManager:
    # This class is responsible for talking to the Google Sheet.

    def __init__(self):
        response = requests.get(url=SHEETY_URL, auth=SHEETY_AUTH)
        response.raise_for_status()
        self.google_sheet_data = response.json()
        self.cities = []
        self.iata_codes = []
        self.lowest_prices = []
        self.row_numbers = []
        self.customer_data = []
        for data in self.google_sheet_data["prices"][0:]:
            self.cities += [data["city"]]
            self.iata_codes += [data["iataCode"]]
            self.lowest_prices += [data["lowestPrice"]]
            self.row_numbers += [data["id"]]


    def upload_iata_to_sheet(self, row_number, iata_code):
        # Upload to google sheets
        endpoint = f"{SHEETY_URL}/{row_number}"
        params = {"price": {"iataCode": iata_code}}
        response = requests.put(url=endpoint, json=params, auth=SHEETY_AUTH)
        response.raise_for_status()

    def get_customer_emails(self):
        customers_endpoint = SHEETY_USERS_URL
        response = requests.get(customers_endpoint, auth=SHEETY_AUTH)
        data = response.json()
        self.customer_data = data["users"]
        return self.customer_data

