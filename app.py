import sqlite3
from flask import Flask, redirect, render_template, request, session


app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True


connection = sqlite3.connect("birthdays.db", check_same_thread=False)
cursor = connection.cursor()


@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form.get("nameInput")
        month = request.form.get("monthInput")
        day = request.form.get("dayInput")

        cursor.execute("INSERT INTO birthdays (name, month, day) VALUES(?, ?, ?)", (name, month, day))
        connection.commit()

        return redirect("/")

    else:
        people = cursor.execute("SELECT name, month, day FROM birthdays ORDER BY id DESC").fetchall()

        return render_template("index.html", people=people)


