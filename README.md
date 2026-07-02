# PrettyGoodAIVoiceBotChallenge

This is my voice bot for the Pretty Good AI engineering challenge. It acts as a patient, calls the Pretty Good AI test line, records the calls, and helps me test how the receptionist handles scheduling, refills, cancellations, insurance questions, office hours, and edge cases.

## What is included

- `app.py` - Flask webhook that Twilio calls during the phone conversation.
- `test_call.py` - starts an outbound call to the Pretty Good AI test number.
- `scenarios.py` - patient scenarios used for each test call.
- `recordings/` - final MP3 recordings for the selected 10 calls.
- `logs/` - saved call logs/transcripts from the selected 10 calls.
- `BUG_REPORT.md` - main bug report based on the final MP3s.
- `bug_reports/` - per-call notes for the final 10 calls.
- `PrettyGoodAI_Explanation.pdf` - short architecture/design explanation.

## Setup

1. Create and activate a virtual environment.

```bash
python -m venv .venv
.venv\Scripts\activate
```

2. Install the Python packages.

```bash
pip install -r requirements.txt
```

3. Copy `.env.example` to `.env` and fill in the real values.

```bash
copy .env.example .env
```

Required environment variables:

- `TWILIO_ACCOUNT_SID`
- `TWILIO_AUTH_TOKEN`
- `TWILIO_PHONE_NUMBER`
- `OPENAI_API_KEY`
- `CURRENT_SCENARIO`

`CURRENT_SCENARIO` can be one of the scenario names in `scenarios.py`, such as `back_pain`, `refill`, `cancel`, `office_hours`, `insurance`, `reschedule`, or `new_patient`.

## Running a call

Start the Flask server:

```bash
python app.py
```

Expose the local server with ngrok:

```bash
ngrok http 5000
```

Update the webhook URL in `test_call.py` so it points to your ngrok `/voice` URL, then start the outbound call:

```bash
python test_call.py
```

The call is placed to the Pretty Good AI assessment number. The Twilio call is recorded, and I saved the final selected recordings in `recordings/`.

## Final call set

I selected these 10 final calls:

- Call 5
- Call 6
- Call 7
- Call 8
- Call 9
- Call 10
- Call 11
- Call 12
- Call 13
- Call 15

The matching MP3s are in `recordings/`, the logs are in `logs/`, and the per-call notes are in `bug_reports/`.

## Bug report notes

The main bug report is `BUG_REPORT.md`. I based the final bug notes on the MP3s because the text transcripts do not always match the audio exactly.

## Submission checklist

- Public GitHub repo link
- Architecture/design explanation
- Loom walkthrough link
- Loom or screen recording showing AI-assisted debugging/fixing
- One phone number used for all test calls, in E.164 format
- Final 10 MP3 recordings
- Final 10 logs/transcripts
- Main bug report and per-call bug notes
