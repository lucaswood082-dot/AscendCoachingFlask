from flask import Flask, render_template, request
import os
import requests
import smtplib
from email.mime.text import MIMEText

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

# --------- SETTINGS ---------
GOOGLE_WEBHOOK_URL = "https://script.google.com/macros/s/AKfycby00GsfUEA-OEkqs-cQromJLK26L-m8KcON--gngoBeWg1uY5sfWQkNKXmYG0UiARRBVg/exec"
ADMIN_EMAIL = "woojoowood01@gmail.com"   # where notifications get sent
SMTP_EMAIL = "woojoowood01@gmail.com"       # Gmail you send FROM
SMTP_PASSWORD = "bhhy vcyy tqno imjy"      # Gmail app password (not account password!)
# ----------------------------


# -------- EMAIL FUNCTION --------
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

# -------- SEND TO GOOGLE SHEETS --------
def send_to_sheet(data):
    try:
        requests.post(GOOGLE_WEBHOOK_URL, json=data)
    except Exception as e:
        print("Google Sheet Error:", e)


# ----------- ROUTES -------------
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


# ---------- PROGRAM REQUEST ----------
@app.route("/get_program/<program>", methods=["GET", "POST"])
def get_program(program):
    if request.method == "POST":
        email = request.form.get("email")

        if not email:
            return render_template("get_program.html", program=program, error="Please enter a valid email.")

        # SEND TO SHEET
        send_to_sheet({
            "form_type": "Program Request",
            "email": email,
            "program": program
        })

        # EMAIL NOTIFY YOU
        send_email_notification(
            subject=f"New Program Request: {program}",
            message=f"Email: {email}\nProgram: {program}"
        )

        return render_template(
            "submit_success.html",
            title="Program Sent",
            message=f"Thanks! The {program.capitalize()} program has been sent to {email}."
        )

    return render_template("get_program.html", program=program, error=None)


# ---------- CONTACT FORM ----------
@app.route("/submit_contact", methods=["POST"])
def submit_contact():
    name = request.form.get("name")
    contact_info = request.form.get("contact")
    goals = request.form.get("goals")

    if not name or not contact_info or not goals:
        return render_template("contact.html", error="Please fill out all required fields.")

    # SEND TO SHEET
    send_to_sheet({
        "form_type": "Coaching Contact",
        "name": name,
        "contact": contact_info,
        "goals": goals
    })

    # EMAIL YOU
    send_email_notification(
        subject="New Coaching Contact",
        message=f"Name: {name}\nContact: {contact_info}\nGoals: {goals}"
    )

    return render_template(
        "submit_success.html",
        title="Signup Received",
        message=f"Thanks {name}! We'll reach out via {contact_info}."
    )


# ---------- NEWSLETTER ----------
@app.route("/newsletter", methods=["POST"])
def newsletter():
    email = request.form.get("email")

    if not email:
        return render_template("contact.html", error="Please provide a valid email.")

    # SEND TO SHEET
    send_to_sheet({
        "form_type": "Newsletter Signup",
        "email": email
    })

    # EMAIL YOU
    send_email_notification(
        subject="New Newsletter Signup",
        message=f"Email: {email}"
    )

    return render_template(
        "submit_success.html",
        title="Newsletter Subscribed",
        message=f"{email} has been added to the mailing list."
    )


# -------- RUN APP ----------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)
