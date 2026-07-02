# Bug Report

Final calls: 5, 6, 7, 8, 9, 10, 11, 12, 13, and 15.

Quick note: I used the MP3s for these notes. The transcripts are useful, but they do not always match the audio, so I did not rely on exact transcript wording or timestamps here.

## 1. Interruptions and turn-taking

Severity: Medium

Calls: `recordings/call5.mp3`, `recordings/call6.mp3`, `recordings/call7.mp3`, `recordings/call9.mp3`, `recordings/call10.mp3`, `recordings/call12.mp3`

What happened: A few calls still had people talking over each other.

- Call 5: The patient caller came in too fast while the receptionist was still talking.
- Call 6: The caller stopped responding to the recording notice, which was better, but the greeting still got interrupted. There was also overlap when options were being read back.
- Call 7: The opening greeting was interrupted.
- Call 9: The receptionist cut in while the patient was introducing themself.
- Call 10: The receptionist interrupted while the patient was talking.
- Call 12: The receptionist cut into the patient's clarification.

Why it matters: These calls are judged on voice quality first. Even if the task gets done, overlap makes the call feel less real and can hide important details.

What I would change: Let the receptionist finish greetings, options, and readbacks before the patient answers. Also give the patient a little more room to finish a sentence before the receptionist jumps in.

## 2. Greeting delay

Severity: Low

Calls: `recordings/call8.mp3`, `recordings/call9.mp3`, `recordings/call10.mp3`, `recordings/call12.mp3`, `recordings/call13.mp3`, `recordings/call15.mp3`

What happened: The start of the call still felt slow in a few recordings.

- Call 8: Long wait during the intro, and the receptionist asked twice if this was John.
- Call 9: Slow greeting response.
- Call 10: Long wait before the greeting.
- Call 12: Greeting was slow.
- Call 13: Initial greeting still had delay.
- Call 15: Greeting was okay, but it could still be a little faster.

Why it matters: Slow openings make the patient caller more likely to start talking too soon.

What I would change: Keep the patient from interrupting, but tighten the greeting delay so the opening feels more natural.

## 3. Pauses and timeout behavior

Severity: Medium

Calls: `recordings/call9.mp3`, `recordings/call10.mp3`, `recordings/call11.mp3`

What happened: Timeout handling got better, but it still needs tuning.

- Call 9: Timeout response was good, but the patient caller could use better fallback lines like "Hello, are you still there?"
- Call 10: When the receptionist said "one moment," the patient caller could get pulled into a timeout loop.
- Call 11: Timeout response was good overall, but the caller still needs to wait better when the receptionist is typing or processing.

Why it matters: A pause does not always mean the receptionist is done. Sometimes it means the receptionist is working.

What I would change: Treat "one moment" as a hold. Wait longer before speaking again, and only use a clarification line after a real silence.

## 4. Transfer flow

Severity: Medium

Call: `recordings/call8.mp3`

What happened: The transfer call was handled pretty well, but the receptionist kept trying to help after the patient had already asked for support. Since the receptionist did not have the information the patient needed, that part felt circular.

Why it matters: If the patient asks for support because the receptionist cannot answer the question, the call should not keep looping through the bot.

What I would change: Once the patient asks for support in that situation, transfer right away.

## 5. Scenario setup from the patient side

Severity: Low

Calls: `recordings/call5.mp3`, `recordings/call9.mp3`, `recordings/call10.mp3`

What happened: A few issues came from the patient caller setup, not only from the receptionist.

- Call 5: The patient should give a clearer reason for rescheduling.
- Call 9: The refill scenario should already have a pharmacy name and address ready.
- Call 10: The patient should only give their name during the greeting, then wait for the receptionist to ask how it can help before giving the refill request.

Why it matters: The patient caller needs to sound like a real patient, not like it is dumping the whole script at once.

What I would change: Answer the receptionist's current question first. Give the bigger scenario details after the receptionist asks for them.

## 6. Calls that worked well

Severity: Informational

Calls: `recordings/call7.mp3`, `recordings/call8.mp3`, `recordings/call11.mp3`, `recordings/call13.mp3`, `recordings/call15.mp3`

What worked:

- Call 7: Good cancellation reason and good follow-up about the confirmation number.
- Call 8: Good follow-up about appointment details, and the call ended well.
- Call 11: Faster greeting, good phone number correction, good timeout response, and a clean ending.
- Call 13: Good overall conversation.
- Call 15: Good wait time while the receptionist was typing, good follow-up questions, and no interruption at the end.

Why it matters: These calls show the caller improved over time. I would keep these behaviors and keep tuning timing, turn-taking, and pauses.
