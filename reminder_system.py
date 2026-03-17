import datetime
import smtplib
import json
from email.mime.text import MIMEText

# 📧 EMAIL CONFIG
SENDER = "ayeshabhanu788@gmail.com"
RECEIVER = "ayeshabhanu788@gmail.com"
PASSWORD = "abkvjmgfddfbfvio"

# 📁 Load reminders
with open("reminders.json", "r") as f:
    reminders = json.load(f)

now = (datetime.datetime.utcnow() + datetime.timedelta(hours=5, minutes=30)).strftime("%H:%M")

for r in reminders:
    if now >= r["time"]:
        task = r["task"]
        print(f"🔔 Sending reminder: {task}")

        msg = MIMEText(f"Reminder: {task}")
        msg["Subject"] = "Task Reminder"
        msg["From"] = SENDER
        msg["To"] = RECEIVER

        try:
            with smtplib.SMTP("smtp.gmail.com", 587) as server:
                server.starttls()
                server.login(SENDER, PASSWORD)
                server.send_message(msg)

            print("✅ Email sent")

        except Exception as e:
            print("❌ Error:", e)
