# Flight Deals
Searches through upcoming flight data to find deals on upcoming flights. If flight deals are found an email or text will be sent notifying of the deals.

Variable "ORIGIN_CITY_IATA" within main.py needs to be adjusted to the IATA code of the desired city of origin.

To use associated APIs, accounts need to be created with Sheety, Tequila (by Kiwi), and Twilio.

Environment Variables:
- SHEETY_URL
- SHEETY_USERS_URL
- SHEETY_AUTH
- TEQUILA_URL
- AffilID
- API_KEY
- TWILIO_ACCOUNT_SID
- TWILIO_AUTH_TOKEN
- FROM_PHONE_NUMBER
- TO_PHONE_NUMBER
- SENDER_EMAIL
- SENDER_PASSWORD
