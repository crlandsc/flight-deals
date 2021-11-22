import smtplib
from twilio.rest import Client

TWILIO_ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN")
FROM_PHONE_NUMBER = os.environ.get("FROM_HONE_NUMBER")
TO_PHONE_NUMBER = os.environ.get("TO_PHONE_NUMBER")
SENDER_EMAIL = os.environ.get("SENDER_EMAIL")
SENDER_PASSWORD = os.environ.get("SENDER_PASSWORD")


class NotificationManager:
    # This class is responsible for sending notifications with the deal flight details.

    def __init__(self):
        self.client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

    def text_to_phone(self, message):
        message = self.client.messages.create(
            body=message,
            from_=FROM_PHONE_NUMBER,
            to=TO_PHONE_NUMBER
        )
        # Prints if successfully sent.
        # print(message.sid)

    def send_emails(self, emails, message, google_flight_link):
        with smtplib.SMTP("smtp.gmail.com", 587) as connection:
            connection.starttls()
            sender_email = SENDER_EMAIL
            sender_password = SENDER_PASSWORD
            connection.login(sender_email, sender_password)
            for email in emails:
                connection.sendmail(
                    from_addr=sender_email,
                    to_addrs=email,
                    msg=f"Subject:New Low Price Flight!\n\n{message}\n{google_flight_link}".encode('utf-8')
                )
