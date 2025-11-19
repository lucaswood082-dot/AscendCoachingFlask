from flask import Flask, render_template, request
import os

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

# --- Main Pages ---
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


# --- Optimal Hub ---
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


# --- Program Signup ---
@app.route("/get_program/<program>", methods=["GET", "POST"])
def get_program(program):
    if request.method == "POST":
        email = request.form.get("email")
        if not email:
            return render_template(
                "get_program.html",
                program=program,
                error="Please enter a valid email."
            )
        print(f"Program '{program}' requested by email: {email}")
        return render_template(
            "submit_success.html",
            title="Program Sent",
            message=f"Thanks! The {program.capitalize()} program has been sent to {email}."
        )
    return render_template("get_program.html", program=program, error=None)


# --- Contact + Newsletter Forms ---
@app.route("/submit_contact", methods=["POST"])
def submit_contact():
    name = request.form.get("name")
    contact_info = request.form.get("contact")
    goals = request.form.get("goals")
    if not name or not contact_info or not goals:
        return render_template(
            "contact.html",
            error="Please fill out all required fields."
        )
    print("Coaching Signup:", name, contact_info, goals)
    return render_template(
        "submit_success.html",
        title="Signup Received",
        message=f"Thanks {name}! We'll reach out via {contact_info}."
    )

@app.route("/newsletter", methods=["POST"])
def newsletter():
    email = request.form.get("email")
    if not email:
        return render_template(
            "contact.html",
            error="Please provide a valid email."
        )
    print("Newsletter:", email)
    return render_template(
        "submit_success.html",
        title="Newsletter Subscribed",
        message=f"{email} has been added to the mailing list."
    )


# --- Run App ---
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))  # default to 8000 instead of 5000
    app.run(host="0.0.0.0", port=port)

