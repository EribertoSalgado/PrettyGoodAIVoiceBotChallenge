import os
from dotenv import load_dotenv
from twilio.rest import Client

load_dotenv()

account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")
twilio_number = os.getenv("TWILIO_PHONE_NUMBER")

client = Client(account_sid, auth_token)

print("Creating outbound call...")

call = client.calls.create(
    to="+18054398008",
    from_=twilio_number,
    url="https://stucco-fencing-sequence.ngrok-free.dev/voice",
    method="POST",
    record=True
)

print("Call SID:", call.sid)
print("Status:", call.status)