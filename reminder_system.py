import datetime
import smtplib
import json
from email.mime.text import MIMEText

# EMAIL CONFIG
SENDER = "ayeshabhanu788@gmail.com"
RECEIVER = "noorit245@gmail.com"
PASSWORD = "abkvjmgfddfbfvio"  # ⚠️ put NEW app password (no spaces)

# Convert UTC → IST
current_dt = datetime.datetime.utcnow() + datetime.timedelta(hours=5, minutes=30)
today = str(datetime.date.today())

# Load reminders
with open("reminders.json", "r") as f:
    reminders = json.load(f)

# Prevent duplicate sending
sent_file = "sent_log.txt"
try:
    with open(sent_file, "r") as f:
        sent = f.read().splitlines()
except:
    sent = []

for r in reminders:
    unique_id = r["task"] + today

    # Convert reminder time
    target_time = datetime.datetime.strptime(r["time"], "%H:%M")
    target_dt = current_dt.replace(hour=target_time.hour, minute=target_time.minute, second=0, microsecond=0)

    # Difference in seconds
    diff = (current_dt - target_dt).total_seconds()

    # Check within 1 minute window
    if 0 <= diff <= 60 and unique_id not in sent:
        msg = MIMEText(f"Reminder: {r['task']}")
        msg["Subject"] = "Task Reminder"
        msg["From"] = SENDER
        msg["To"] = RECEIVER

        try:
            with smtplib.SMTP("smtp.gmail.com", 587) as server:
                server.starttls()
                server.login(SENDER, PASSWORD)
                server.send_message(msg)

            print("✅ Email sent")

            # Save log to avoid duplicate
            with open(sent_file, "a") as f:
                f.write(unique_id + "\n")

        except Exception as e:
            print("❌ Error:", e)
