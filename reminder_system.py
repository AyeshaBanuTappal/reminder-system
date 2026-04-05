import datetime
import smtplib
import json
import os
from email.mime.text import MIMEText

SENDER = "ayeshabhanu788@gmail.com"
RECEIVER = "lasya.d2007@gmail.com"
PASSWORD = os.environ.get("EMAIL_PASS")

# Current IST time
current_dt = datetime.datetime.utcnow() + datetime.timedelta(hours=5, minutes=30)

# Load reminders
with open("reminders.json", "r") as f:
    reminders = json.load(f)

# Prevent duplicate emails
sent = set()

for r in reminders:
    target_time = datetime.datetime.strptime(r["time"], "%H:%M")
    target_dt = current_dt.replace(
        hour=target_time.hour,
        minute=target_time.minute,
        second=0,
        microsecond=0
    )

    diff = (current_dt - target_dt).total_seconds()

    print("Current:", current_dt.strftime("%H:%M"))
    print("Target:", r["time"])
    print("Diff:", diff)

    unique_id = r["task"] + str(current_dt.date())

    # FINAL CONDITION (no miss)
    if diff >= 0 and unique_id not in sent:
        try:
            print("Trying to send email...")

            msg = MIMEText(f"Reminder: {r['task']}")
            msg["Subject"] = "Task Reminder"
            msg["From"] = SENDER
            msg["To"] = RECEIVER

            with smtplib.SMTP("smtp.gmail.com", 587) as server:
                server.starttls()
                server.login(SENDER, PASSWORD)
                server.send_message(msg)

            print("✅ Email sent")
            sent.add(unique_id)

        except Exception as e:
            print("❌ Error:", e)
