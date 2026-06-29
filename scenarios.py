# --------------------------------------------------------------------
# Pretty Good AI Voice Bot Challenge
# Author: Eriberto Salgado
#
# File: scenarios.py
#
# This file contains all of the patient scenarios used during testing.
# Each scenario gives the AI patient a different goal so the receptionist
# can be tested with different types of healthcare conversations.
# --------------------------------------------------------------------

# Dictionary containing all available test scenarios
SCENARIOS = {

    # Schedule a basic checkup
    "appointment": """
    Goal: Schedule a routine general checkup.
    Preference: Wednesday or Thursday morning.
    If offered a matching appointment, accept it clearly.
    """,

    # Change an existing appointment
    "reschedule": """
    Goal: Reschedule an existing appointment.
    Current appointment: Tuesday at 2:00 PM.
    New preference: Next week in the morning.
    """,

    # Cancel an appointment and ask for confirmation
    "cancel": """
    Goal: Cancel an appointment scheduled for tomorrow.
    Ask if there is a cancellation confirmation number.
    """,

    # Request a prescription refill
    "refill": """
    Goal: Request a medication refill.
    Medication: Lisinopril.
    Situation: You have three pills left and no refills remaining.
    Ask what information is needed only after the receptionist asks follow-up questions.
    """,

    # Ask about insurance before scheduling
    "insurance": """
    Goal: Ask whether Blue Cross Blue Shield is accepted.
    If yes, ask to schedule a routine appointment.
    """,

    # Ask about office hours and weekends
    "office_hours": """
    Goal: Ask about office hours.
    Then ask whether weekend appointments are available.
    """,

    # Ask where the office is located
    "location": """
    Goal: Ask for the office location and parking information.
    Then ask if you can schedule at that location.
    """,

    # New patient asking about first visit requirements
    "new_patient": """
    Goal: Ask what a new patient needs before a first visit.
    Then schedule the earliest available appointment.
    """,

    # Orthopedic appointment for back pain
    "back_pain": """
    Goal: Schedule an orthopedic appointment for lower back pain.
    Preference: Morning appointment.
    If the receptionist says an appointment already exists, ask to confirm or reschedule that appointment instead of requesting a duplicate appointment.
    If offered a matching appointment, accept it.
    """,

    # Used to test how the receptionist handles unclear requests
    "edge_case_unclear": """
    Goal: Test unclear requests.
    Start vague, then clarify that you want an appointment.
    Occasionally ask the receptionist to repeat information.
    """
}