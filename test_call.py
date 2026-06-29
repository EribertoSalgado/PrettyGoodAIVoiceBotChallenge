# --------------------------------------------------------------------
# Pretty Good AI Voice Bot Challenge
# Author: Eriberto Salgado
# Python Version: 3.13.12
#
# File: test_call.py
#
# This script starts an outbound phone call using Twilio.
# It loads the Twilio credentials from the .env file,
# places the call to the Pretty Good AI phone number,
# and tells Twilio where to get the call instructions
# from the Flask application.
# --------------------------------------------------------------------

import os
from dotenv import load_dotenv
from twilio.rest import Client

# Load environment variables from the .env file
load_dotenv()

# Read the Twilio account information
account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")
twilio_number = os.getenv("TWILIO_PHONE_NUMBER")

# Create the Twilio client
client = Client(account_sid, auth_token)

print("Creating outbound call...")

# Start the phone call
call = client.calls.create(
    # Pretty Good AI assessment phone number
    to="+18054398008",

    # Twilio phone number used to make the call
    from_=twilio_number,

    # Webhook that tells Twilio how to handle the conversation
    url="https://stucco-fencing-sequence.ngrok-free.dev/voice",

    # Send requests to the webhook using POST
    method="POST",

    # Record the call for testing and review
    record=True
)

# Display the call information
print("Call SID:", call.sid)
print("Status:", call.status)