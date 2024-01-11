import csv

from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from forms import RegisterForm, LoginForm


app = Flask(__name__)

Bootstrap5(app)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/add_cafe")
def add_cafe():
    return render_template("add_cafe.html")


@app.route("/remove_cafe")
def remove_cafe():
    return render_template("remove_cafe.html")


@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        form_data = request.form
        with open("suggestions_form.csv", "a", newline= "" ) as file:
            writer = csv.writer(file)
            writer.writerow([form_data["name"], form_data["email"], form_data["subject"], form_data["message"]])
            return render_template("contact.html", msg_sent=True)
    return render_template("contact.html", msg_sent=False)


@app.route("/sign_up")
def sign_up():
    return render_template("register.html")


if __name__ == "__main__":
    app.run(debug=True)