import datetime
import smtplib
import json
from email.mime.text import MIMEText

# EMAIL CONFIG
SENDER = "ayeshabhanu788@gmail.com"
RECEIVER = "ayeshabhanu788@gmail.com"
PASSWORD = "bdfnetihzyktpclv"  # ⚠️ put NEW app password (no spaces)

# Convert UTC → IST
REMINDER_FILE = "reminders.json"
SENT_FILE = "sent_log.txt"

def load_sent():
    try:
        with open(SENT_FILE, "r") as f:
            return f.read().splitlines()
    except:
        return []

def save_sent(unique_id):
    with open(SENT_FILE, "a") as f:
        f.write(unique_id + "\n")

def send_email(task):
    msg = MIMEText(f"Reminder: {task}")
    msg["Subject"] = "Task Reminder"
    msg["From"] = SENDER
    msg["To"] = RECEIVER

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(SENDER, PASSWORD)
        server.send_message(msg)

while True:
    try:
        # Current IST time
        current_dt = datetime.datetime.utcnow() + datetime.timedelta(hours=5, minutes=30)
        today = str(current_dt.date())

        # Load reminders
        with open(REMINDER_FILE, "r") as f:
            reminders = json.load(f)

        sent = load_sent()

        for r in reminders:
            unique_id = r["task"] + today

            # Convert reminder time
            target_time = datetime.datetime.strptime(r["time"], "%H:%M")
            target_dt = current_dt.replace(
                hour=target_time.hour,
                minute=target_time.minute,
                second=0,
                microsecond=0
            )

            diff = (current_dt - target_dt).total_seconds()

            # ✅ FIXED CONDITION (no missing)
            if diff >= 0 and unique_id not in sent:
                try:
                    send_email(r["task"])
                    print(f"✅ Email sent: {r['task']}")
                    save_sent(unique_id)
                except Exception as e:
                    print("❌ Email error:", e)

    except Exception as e:
        print("❌ General error:", e)

    # Check every 30 seconds
    time.sleep(30)
