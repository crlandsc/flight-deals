import requests
from flight_data import FlightData

TEQUILA_URL = os.environ.get("TEQUILA_URL")
AffilID = os.environ.get("AffilID")
API_KEY = os.environ.get("API_KEY")


class FlightSearch:
    # This class is responsible for talking to the Flight Search API.

    def __init__(self):
        pass

    def get_IATA_code(self, city):
        # Return the IATA cose for each city in the spreadsheet
        endpoint = f"{TEQUILA_URL}/locations/query"
        headers = {"apikey": API_KEY}
        query = {
            "term": city,
            "locale": "en-US",
            "location_types": "airport",
        }

        response = requests.get(url=endpoint, params=query, headers=headers)
        response.raise_for_status()
        return response.json()["locations"][0]["id"]


    def search_cheapest_flights(self, departure_iata_code, destination_iata_code, date_from, date_to):
        # Search for cheapest flights from tomorrow to 6 months from now
        endpoint = f"{TEQUILA_URL}/v2/search"
        headers = {"apikey": API_KEY}
        query = {
            "fly_from": departure_iata_code,
            "fly_to": destination_iata_code,
            "date_from": date_from.strftime("%d/%m/%Y"),
            "date_to": date_to.strftime("%d/%m/%Y"),
            "nights_in_dst_from": 7,
            "nights_in_dst_to": 28,
            "flight_type": "round",
            "one_for_city": 1,
            "max_stopovers": 0,
            "curr": "USD"
        }

        response = requests.get(url=endpoint, params=query, headers=headers)
        response.raise_for_status()
        # print(response.json())

        try:
            data = response.json()["data"][0]
        except IndexError:
            query["max_stopovers"] = 1
            response = requests.get(url=endpoint, params=query, headers=headers)
            # response.raise_for_status()
            # print(response.json())
            if response.json()["data"]:
                data = response.json()["data"][0]
                # print(data)
                flight_data = FlightData(
                    price=data["price"],
                    origin_city=data["route"][0]["cityFrom"],
                    origin_airport=data["route"][0]["flyFrom"],
                    destination_city=data["route"][1]["cityTo"],
                    destination_airport=data["route"][1]["flyTo"],
                    out_date=data["route"][0]["local_departure"].split("T")[0],
                    return_date=data["route"][2]["local_departure"].split("T")[0],
                    stop_overs=1,
                    via_city=data["route"][0]["cityTo"]
                )
                print(f"{flight_data.destination_city}: ${flight_data.price} with 1 layover in {flight_data.via_city}")
                return flight_data
            else:
                print("No flights with 0 or 1 layover.")

        else:
            flight_data = FlightData(
                price=data["price"],
                origin_city=data["route"][0]["cityFrom"],
                origin_airport=data["route"][0]["flyFrom"],
                destination_city=data["route"][0]["cityTo"],
                destination_airport=data["route"][0]["flyTo"],
                out_date=data["route"][0]["local_departure"].split("T")[0],
                return_date=data["route"][1]["local_departure"].split("T")[0]
            )
            # print(f"{flight_data.destination_city}: ${flight_data.price}")
            return flight_data

