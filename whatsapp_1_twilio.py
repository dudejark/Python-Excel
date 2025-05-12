from twilio.rest import Client
import os

def send_whatsapp(message_text):
    account_sid = os.getenv("ACCOUNT_SID")
    auth_token = os.getenv("AUTH_TOKEN")
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        body=message_text,
        from_=os.getenv("TWILIO_SANDBOX_NUMBER"),  # Twilio sandbox number
        to=os.getenv("RECEIVER_WHATSAPP_NUMBER")     # Your verified WhatsApp number
    )

    print("WhatsApp message sent:", message.sid)

send_whatsapp("hello Mamta Dudeja! This is a test message from Ram. How are you?")