# 🚀 Smart Email Reminder System using Python

A simple automation project that sends email reminders for scheduled tasks using Python.  
It ensures reminders are sent only once, even if the script restarts.

---

## 📌 Features

- ⏰ Sends email reminders at scheduled time (IST supported)
- 🔁 Prevents duplicate emails using persistent storage
- 📂 Stores tasks using JSON
- 🔐 Uses environment variables for secure authentication
- ⚡ Lightweight and easy to use

---

## 🛠 Tech Stack

- Python 🐍
- SMTP (Email Automation)
- JSON
- Datetime Module

---


## 📁 Project Structure

reminder_system.py   # Main script  
reminders.json       # Task list  
sent.json            # Tracks sent reminders 
---

## ⚙️ How It Works

1. Loads tasks from `reminders.json`
2. Gets current IST time
3. Compares with scheduled time
4. Sends email if:
   - Time matches (within 1 minute window)
   - Task not already sent
5. Saves sent tasks in `sent.json`

---

## 🚀 Setup

### 1. Set Gmail App Password

⚠️ Do NOT use your normal Gmail password

export EMAIL_PASS="your_app_password"

---

### 2. Add reminders

[
  {"task": "Drink water", "time": "18:30"},
  {"task": "Study DSA", "time": "20:00"}
]

---

### 3. Run

python reminder_system.py

---

## 🧠 What I Learned

- Python automation  
- Time-based logic  
- Avoiding duplicate execution  
- Using environment variables  

---

## 🚀 Future Improvements

- WhatsApp / Telegram alerts  
- Web dashboard  
- Recurring reminders  
---

⭐ If you like this project, give it a star!
