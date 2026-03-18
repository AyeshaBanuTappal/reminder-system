import datetime
import smtplib
import json
import os
from email.mime.text import MIMEText

# EMAIL CONFIG
SENDER = "ayeshabhanu788@gmail.com"
RECEIVER = "ayeshabhanu788@gmail.com"
PASSWORD = os.getenv("EMAIL_PASS")

REMINDER_FILE = "reminders.json"

def send_email(task):
    msg = MIMEText(f"Reminder: {task}")
    msg["Subject"] = "Task Reminder"
    msg["From"] = SENDER
    msg["To"] = RECEIVER

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(SENDER, PASSWORD)
        server.send_message(msg)

# 🔥 MAIN CODE STARTS HERE (OUTSIDE FUNCTION)

try:
    current_dt = datetime.datetime.utcnow() + datetime.timedelta(hours=5, minutes=30)

    with open(REMINDER_FILE, "r") as f:
        reminders = json.load(f)

    for r in reminders:
        target_time = datetime.datetime.strptime(r["time"], "%H:%M")
        target_dt = current_dt.replace(
            hour=target_time.hour,
            minute=target_time.minute,
            second=0,
            microsecond=0
        )

        diff = (current_dt - target_dt).total_seconds()

        # ✅ 3 min safe window
        if 0 <= diff <= 180:
            send_email(r["task"])
            print(f"✅ Email sent: {r['task']}")

except Exception as e:
    print("❌ Error:", e)
