from flask import Flask, render_template, request, redirect, url_for
import db_functions
import mysql.connector

db = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="password",
    database="vision_attendance"
)

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        u = request.form['username']
        p = request.form['password']
        user = db_functions.get_login(db, u, p)
        if user[0] == -1:
            error = "Invalid credentials, please try again"

        if user[0] == 0:
            #student
            attendances = db_functions.get_attendance_percentages(db, user[1])
            return render_template("student.html", sid = user[1], name = user[2], attendances = attendances)

        if user[0] == 1:
            #prof
            return render_template("professor.html", pid = user[1])
    
    return render_template("login2.html", error=error)

@app.route("/professor")
def professor():    
   return "hello world"

if __name__ == "__main__":
    app.run(debug = True)
