import datetime
import smtplib
import json
import os
from email.mime.text import MIMEText

SENDER = "ayeshabhanu788@gmail.com"
RECEIVER = "ayeshabhanu788@gmail.com"
PASSWORD = os.getenv("EMAIL_PASS")

current_dt = datetime.datetime.utcnow() + datetime.timedelta(hours=5, minutes=30)

with open("reminders.json", "r") as f:
    reminders = json.load(f)

# avoid duplicates in same run
sent = set()

for r in reminders:
    target_time = datetime.datetime.strptime(r["time"], "%H:%M")
    target_dt = current_dt.replace(hour=target_time.hour, minute=target_time.minute)

    diff = (current_dt - target_dt).total_seconds()
    unique_id = r["task"] + str(current_dt.date())

    if 0 <= diff <= 600 and unique_id not in sent:
        try:
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
