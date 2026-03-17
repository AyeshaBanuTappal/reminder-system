import datetime
import smtplib
import json
from email.mime.text import MIMEText

SENDER = "ayeshabhanu788@gmail.com"
RECEIVER = "noorit245@gmail.com"
PASSWORD = "abkvjmgfddfbfvio"
# Convert UTC → IST
current_time = (datetime.datetime.utcnow() + datetime.timedelta(hours=5, minutes=30)).strftime("%H:%M")
today = str(datetime.date.today())

with open("reminders.json", "r") as f:
    reminders = json.load(f)

# prevent duplicate sending
sent_file = "sent_log.txt"
try:
    with open(sent_file, "r") as f:
        sent = f.read().splitlines()
except:
    sent = []

for r in reminders:
    unique_id = r["task"] + today

    if current_time == r["time"] and unique_id not in sent:
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

            with open(sent_file, "a") as f:
                f.write(unique_id + "\n")

        except Exception as e:
            print("❌ Error:", e)

            
