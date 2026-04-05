import datetime
import smtplib
import json
import os
from email.mime.text import MIMEText

SENDER = "ayeshabhanu788@gmail.com"
RECEIVER = "edigarajesh38@gmail.com"
PASSWORD = os.environ.get("EMAIL_PASS")

# Get current IST time
current_dt = datetime.datetime.utcnow() + datetime.timedelta(hours=5, minutes=30)

# Load reminders
with open("reminders.json", "r") as f:
    reminders = json.load(f)

# Load already sent reminders
if os.path.exists("sent.json"):
    with open("sent.json", "r") as f:
        sent = set(json.load(f))
else:
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

    # Send ONLY once within 1 minute window
    if 0 <= diff <= 60 and unique_id not in sent:
        try:
            print("📧 Sending email...")

            msg = MIMEText(f"Reminder: {r['task']}")
            msg["Subject"] = "Task Reminder"
            msg["From"] = SENDER
            msg["To"] = RECEIVER

            with smtplib.SMTP("smtp.gmail.com", 587) as server:
                server.starttls()
                server.login(SENDER, PASSWORD)
                server.send_message(msg)

            print("✅ Email sent")

            # Save sent reminder
            sent.add(unique_id)
            with open("sent.json", "w") as f:
                json.dump(list(sent), f)

        except Exception as e:
            print("❌ Error:", e)

    else:
        print("⏳ Not time yet or already sent")
