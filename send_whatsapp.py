import os
from twilio.rest import Client

def send_whatsapp_message(message):
    account_sid = os.environ['TWILIO_ACCOUNT_SID']
    auth_token = os.environ['TWILIO_AUTH_TOKEN']
    from_number = os.environ['WHATSAPP_NUMBER']
    to_number = os.environ['TO_WHATSAPP_NUMBER']
    
    client = Client(account_sid, auth_token)
    
    client.messages.create(
        body=message,
        from_=f'whatsapp:{from_number}',
        to=f'whatsapp:{to_number}'
    )