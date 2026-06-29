# --------------------------------------------------------------------
# Pretty Good AI Voice Bot Challenge
# Author: Eriberto Salgado
# Python Version: 3.13.12
#
# File: app.py
#
# This Flask app handles the phone conversation between
# the Pretty Good AI receptionist and the AI patient.
# It receives speech from Twilio, sends it to OpenAI,
# keeps track of the conversation, and returns spoken
# responses back to the receptionist.
# --------------------------------------------------------------------

import os
from flask import Flask, request
from dotenv import load_dotenv
from twilio.twiml.voice_response import VoiceResponse, Gather
from openai import OpenAI
from scenarios import SCENARIOS

# Load environment variables from the .env file
load_dotenv()

app = Flask(__name__)

# OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Stores the conversation so the AI remembers previous messages
conversation_history = []

# Pick which patient scenario to run
CURRENT_SCENARIO = os.getenv("CURRENT_SCENARIO", "appointment")

# Basic patient information that the AI can use if asked
PATIENT_DETAILS = """
Patient details:
First name: John
Last name: Smith
Date of birth: January 3, 1990
Phone: 555-123-4567
Email: john.smith@example.com
Insurance: Blue Cross Blue Shield
Pharamcy: CVS Pharmacy, 123 Main Street, Anytown, USA
"""

# Rules to keep responses short and realistic
BASE_RULES = """
Rules:
Answer only as the patient.
Do not narrate actions.
Keep replies short and natural.
Use one or two sentences maximum.
Do not say you are an AI.
Answer the exact question asked.
Stay focused on the current scenario goal.
If the receptionist offers a valid option that matches the scenario, accept it clearly.
If the receptionist asks to confirm your name or asks if they are speaking with John, only answer:
"Yes, this is John Smith."
Do not mention the appointment, refill, medication, or reason for calling in that reply.
Only state the reason for calling after the receptionist asks how they can help in a later turn.
"""

# Build the system prompt using the selected scenario
SYSTEM_PROMPT = f"""
You are acting as a realistic patient calling a medical office.

Scenario:
{SCENARIOS.get(CURRENT_SCENARIO, SCENARIOS["appointment"])}

{PATIENT_DETAILS}

{BASE_RULES}
"""


def fallback_reply(receptionist_message):
    """
    Returns simple rule-based responses if the OpenAI request fails.
    This keeps the phone call going even if there's an API problem.
    """
    text = receptionist_message.lower()
    
    if "am i speaking with john" in text or "is this john" in text or "speaking with" in text:
        return "Yes, this is John."
    elif "how can i help" in text or "how can i assist" in text:
        return "I would like to schedule an appointment."
    elif "first name" in text:
        return "My first name is John."
    elif "last name" in text:
        return "My last name is Smith."
    elif "full name" in text:
        return "My full name is John Smith."
    elif "date of birth" in text or "birthday" in text:
        return "My date of birth is January third, nineteen ninety."
    elif "phone" in text:
        return "My phone number is 555-123-4567."
    elif "email" in text:
        return "My email is john.smith@example.com."
    elif "insurance" in text:
        return "I have Blue Cross Blue Shield."
    elif "demo patient profile" in text:
        return "Yes, that is fine."
    elif "recorded" in text:
        return "Thank you."
    elif "appointment" in text:
        return "I would like the earliest available appointment this week."
    elif "morning" in text or "afternoon" in text or "time" in text:
        return "Morning works best for me, preferably before ten."
    elif "confirm" in text or "does that work" in text:
        return "Yes, that works for me."
    else:
        return "Yes, that sounds good. Please continue."


def ask_llm(receptionist_message):
    """
    Sends the receptionist's message to OpenAI and
    returns the patient's response.
    """

    # Save what the receptionist just said
    conversation_history.append(
        {"role": "user", "content": receptionist_message}
    )

    # Include the system prompt plus the conversation history
    messages = [{"role": "system", "content": SYSTEM_PROMPT}] + conversation_history

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            temperature=0.7,
            max_tokens=80
        )

        reply = response.choices[0].message.content.strip()

    except Exception as e:
        # If something goes wrong, switch to the fallback responses
        print("OpenAI error:", type(e).__name__)
        print(e)
        reply = fallback_reply(receptionist_message)

    # Save the patient's reply for future context
    conversation_history.append(
        {"role": "assistant", "content": reply}
    )

    print("Patient reply:", reply)

    return reply


@app.route("/")
def home():
    # Simple page to verify the server is running
    return "PrettyGoodAI bot server is running!"


@app.route("/voice", methods=["POST"])
def voice():
    # Start every new phone call with a fresh conversation
    conversation_history.clear()

    scenario_text = SCENARIOS.get(CURRENT_SCENARIO, SCENARIOS["appointment"])

    print("Running scenario:", CURRENT_SCENARIO)
    print(scenario_text)

    response = VoiceResponse()

    # Let the receptionist speak first instead of interrupting
    gather = Gather(
        input="speech",
        action="/respond",
        method="POST",
        speech_timeout=2,
        timeout=10,
        language="en-US"
    )

    response.append(gather)

    # If nothing is heard, continue to the response route
    response.redirect("/respond?initial=1", method="POST")

    return str(response)


@app.route("/respond", methods=["POST"])
def respond():
    # Get the speech recognized by Twilio
    receptionist_message = request.form.get("SpeechResult", "")
    print("Receptionist said:", receptionist_message)

    response = VoiceResponse()

    if receptionist_message:
        lower = receptionist_message.lower()

        # Ignore common recording notices and keep listening
        if (
            "may be recorded" in lower
            or "recorded for quality" in lower
            or "quality and training purposes" in lower
            or "one moment" in lower
        ):
            gather = Gather(
                input="speech",
                action="/respond",
                method="POST",
                speech_timeout=2,
                timeout=5,
                language="en-US"
            )

            response.append(gather)
            response.redirect("/respond", method="POST")
            return str(response)

        # End the call if the appointment is finished
        if (
            "you're all set" in lower
            or "you are all set" in lower
            or "have a great day" in lower
            or "you are scheduled" in lower
            or "appointment is scheduled" in lower
            or "goodbye" in lower
        ):
            response.pause(length=1)
            response.say("Thank you. Goodbye.", voice="Polly.Joanna")
            response.hangup()
            return str(response)

        # Generate a patient response using OpenAI
        reply = ask_llm(receptionist_message)

    else:
        # First message if the receptionist stays silent
        if request.args.get("initial") == "1":
            reply = "Hello, I am calling about an appointment."

            conversation_history.append(
                {"role": "assistant", "content": reply}
            )
        else:
            # Ask the receptionist to repeat if nothing was heard
            reply = "Sorry, I did not catch that. Could you repeat it?"

    # Small pause to sound more natural
    response.pause(length=1)

    # Listen for the receptionist's next response
    gather = Gather(
        input="speech",
        action="/respond",
        method="POST",
        speech_timeout="2",
        timeout=10,
        language="en-US"
    )

    # Speak the patient's response
    gather.say(reply, voice="Polly.Joanna")
    response.append(gather)

    # Continue the conversation until the call ends
    response.redirect("/respond", method="POST")

    return str(response)


if __name__ == "__main__":
    # Run the Flask app locally
    app.run(debug=True, port=5000)