import os
from flask import Flask, request
from dotenv import load_dotenv
from twilio.twiml.voice_response import VoiceResponse, Gather
from openai import OpenAI

load_dotenv()

app = Flask(__name__)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

conversation_history = []

SYSTEM_PROMPT = """
You are acting as a realistic patient calling a medical office.

Your goal is to schedule an appointment.

Patient details:
First name: John
Last name: Smith
Date of birth: January 3, 1990
Phone: 555-123-4567
Email: john.smith@example.com
Insurance: Blue Cross Blue Shield

Rules:
Answer only as the patient.
Do not narrate actions.
Keep replies short and natural.
Use one or two sentences maximum.
Do not say you are an AI.
Stay focused on scheduling an appointment.
"""


def fallback_reply(receptionist_message):
    text = receptionist_message.lower()

    if "how can i help" in text or "how can i assist" in text:
        return "I would like to schedule an appointment."
    elif "am i speaking with john" in text or "is this john" in text or "speaking with" in text:
        return "Yes, this is John."
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
    conversation_history.append(
        {"role": "assistant", "content": receptionist_message}
    )

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
        print("OpenAI error:", type(e).__name__)
        print(e)
        reply = fallback_reply(receptionist_message)

    conversation_history.append(
        {"role": "user", "content": reply}
    )

    print("Patient reply:", reply)

    return reply


@app.route("/")
def home():
    return "PrettyGoodAI bot server is running!"


@app.route("/voice", methods=["POST"])
def voice():
    conversation_history.clear()

    opening = "Hello, I would like to schedule an appointment."

    conversation_history.append(
        {"role": "user", "content": opening}
    )

    response = VoiceResponse()

    gather = Gather(
        input="speech",
        action="/respond",
        method="POST",
        speech_timeout="auto",
        timeout=8,
        language="en-US"
    )

    gather.say(opening, voice="Polly.Joanna")
    response.append(gather)

    response.redirect("/respond", method="POST")

    return str(response)


@app.route("/respond", methods=["POST"])
def respond():
    receptionist_message = request.form.get("SpeechResult", "")
    print("Receptionist said:", receptionist_message)

    response = VoiceResponse()

    if receptionist_message:
        lower = receptionist_message.lower()

        if (
            "you're all set" in lower
            or "you are all set" in lower
            or "have a great day" in lower
            or "you are scheduled" in lower
            or "appointment is scheduled" in lower
        ):
            response.pause(length=1)
            response.say("Thank you. Goodbye.", voice="Polly.Joanna")
            response.hangup()
            return str(response)

        reply = ask_llm(receptionist_message)
    else:
        reply = "Sorry, I did not catch that. Could you repeat it?"

    response.pause(length=1)

    gather = Gather(
        input="speech",
        action="/respond",
        method="POST",
        speech_timeout="auto",
        timeout=8,
        language="en-US"
    )

    gather.say(reply, voice="Polly.Joanna")
    response.append(gather)

    response.redirect("/respond", method="POST")

    return str(response)

if __name__ == "__main__":
    app.run(debug=True, port=5000)