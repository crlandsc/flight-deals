from data_manager import DataManager
from flight_search import FlightSearch
from notification_manager import NotificationManager
from datetime import datetime, timedelta

ORIGIN_CITY_IATA = "LON"


# Create data_manager object from DataManager class that contains data in google sheet
data_manager = DataManager()


# Find the IATA codes for each city and replace them in the data_manager object
if data_manager.iata_codes[0] == "":
    flight_search = FlightSearch()
    iata_flight_codes = []
    for city in data_manager.cities:
        iata_flight_codes += [flight_search.get_IATA_code(city)]
    data_manager.iata_codes = iata_flight_codes

    # Upload the IATA codes to the google sheet
    idx = 0
    for row_number in data_manager.row_numbers:
        data_manager.upload_iata_to_sheet(row_number, data_manager.iata_codes[idx])
        idx += 1



price_idx = 0
for destination in data_manager.iata_codes:
    tomorrow = datetime.now() + timedelta(days=1)
    six_month_from_today = datetime.now() + timedelta(days=(6 * 30))
    flight_search = FlightSearch()
    flight_data = flight_search.search_cheapest_flights(departure_iata_code=ORIGIN_CITY_IATA,
                                                        destination_iata_code=destination,
                                                        date_from=tomorrow, date_to=six_month_from_today)

    if flight_data and flight_data.price < data_manager.lowest_prices[price_idx]:

        users = data_manager.get_customer_emails()
        emails = [row["email"] for row in users]
        names = [row["firstName"] for row in users]

        notification_manager = NotificationManager()
        flight_deal_message = f"Low price alert! Only ${flight_data.price} to fly from {flight_data.origin_city}-" \
                              f"{flight_data.origin_airport} to {flight_data.destination_city}-" \
                              f"{flight_data.destination_airport}, from {flight_data.out_date} " \
                              f"to {flight_data.return_date}."
        if flight_data.stop_overs > 0:
            flight_deal_message += f"\nFlight has {flight_data.stop_overs} stop over, via {flight_data.via_city}."
            print(flight_deal_message)

        link = f"https://www.google.co.uk/flights?hl=en#flt={flight_data.origin_airport}." \
               f"{flight_data.destination_airport}.{flight_data.out_date}*{flight_data.destination_airport}." \
               f"{flight_data.origin_airport}.{flight_data.return_date}"

        notification_manager.send_emails(emails, flight_deal_message, link)
        # notification_manager.text_to_phone(message=flight_deal_message) # send text message to phone
    price_idx += 1


