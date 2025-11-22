from flask import Flask, render_template, request
import os
import requests
import smtplib
from email.mime.text import MIMEText
import threading

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

# ---------------- SETTINGS VIA ENV VARIABLES ----------------
GOOGLE_WEBHOOK_URL = os.environ.get("GOOGLE_WEBHOOK_URL")
ADMIN_EMAIL = os.environ.get("ADMIN_EMAIL")
SMTP_EMAIL = os.environ.get("SMTP_EMAIL")
SMTP_PASSWORD = os.environ.get("SMTP_PASSWORD")

if not all([GOOGLE_WEBHOOK_URL, ADMIN_EMAIL, SMTP_EMAIL, SMTP_PASSWORD]):
    raise RuntimeError("Missing one or more required environment variables: GOOGLE_WEBHOOK_URL, ADMIN_EMAIL, SMTP_EMAIL, SMTP_PASSWORD")

# ---------------- EMAIL FUNCTION ----------------
def send_email_notification(subject, message):
    try:
        msg = MIMEText(message)
        msg["Subject"] = subject
        msg["From"] = SMTP_EMAIL
        msg["To"] = ADMIN_EMAIL

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(SMTP_EMAIL, SMTP_PASSWORD)
            server.sendmail(SMTP_EMAIL, ADMIN_EMAIL, msg.as_string())
    except Exception as e:
        print("Email failed:", e)

# ---------------- GOOGLE SHEETS FUNCTION ----------------
def send_to_sheet(data):
    try:
        requests.post(GOOGLE_WEBHOOK_URL, json=data, timeout=5)
    except Exception as e:
        print("Google Sheet Error:", e)

# ---------------- ROUTES ----------------
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/programs")
def programs():
    return render_template("programs.html")

@app.route("/nutrition")
def nutrition():
    return render_template("nutrition.html")

@app.route("/coaching")
def coaching():
    return render_template("coaching.html")

@app.route("/faq")
def faq():
    return render_template("faq.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/optimal")
def optimal():
    return render_template("optimal.html")

@app.route("/optimal_training")
def optimal_training():
    return render_template("optimal_training.html")

@app.route("/optimal_nutrition")
def optimal_nutrition():
    return render_template("optimal_nutrition.html")

@app.route("/optimal_recovery")
def optimal_recovery():
    return render_template("optimal_recovery.html")

@app.route("/supplements")
def supplements():
    return render_template("supplements.html")

@app.route("/calculator")
def calculator():
    return render_template("calculator.html")


# ---------------- PROGRAM REQUEST ----------------
@app.route("/get_program/<program>", methods=["GET", "POST"])
def get_program(program):
    if request.method == "POST":
        email = request.form.get("email")
        if not email:
            return render_template("get_program.html", program=program, error="Please enter a valid email.")

        # run async
        threading.Thread(target=lambda: send_to_sheet({"form_type": "Program Request", "email": email, "program": program})).start()
        threading.Thread(target=lambda: send_email_notification(f"New Program Request: {program}", f"Email: {email}\nProgram: {program}")).start()

        return render_template("submit_success.html",
                               title="Program Sent",
                               message=f"Thanks! The {program.capitalize()} program has been sent to {email}.")

    return render_template("get_program.html", program=program, error=None)

# ---------------- CONTACT FORM ----------------
@app.route("/submit_contact", methods=["POST"])
def submit_contact():
    name = request.form.get("name")
    contact_info = request.form.get("contact")
    goals = request.form.get("goals")

    if not name or not contact_info or not goals:
        return render_template("contact.html", error="Please fill out all required fields.")

    threading.Thread(target=lambda: send_to_sheet({"form_type": "Coaching Contact", "name": name, "contact": contact_info, "goals": goals})).start()
    threading.Thread(target=lambda: send_email_notification("New Coaching Contact", f"Name: {name}\nContact: {contact_info}\nGoals: {goals}")).start()

    return render_template("submit_success.html",
                           title="Signup Received",
                           message=f"Thanks {name}! We'll reach out via {contact_info}.")

# ---------------- NEWSLETTER ----------------
@app.route("/newsletter", methods=["POST"])
def newsletter():
    email = request.form.get("email")
    if not email:
        return render_template("contact.html", error="Please provide a valid email.")

    threading.Thread(target=lambda: send_to_sheet({"form_type": "Newsletter Signup", "email": email})).start()
    threading.Thread(target=lambda: send_email_notification("New Newsletter Signup", f"Email: {email}")).start()

    return render_template("submit_success.html",
                           title="Newsletter Subscribed",
                           message=f"{email} has been added to the mailing list.")

# ---------------- RUN APP ----------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)
