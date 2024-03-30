from flask import Flask, render_template, request, url_for
from flask_mysqldb import MySQL
# import MySQLdb.cursor      
import re

# app.config['MYSQL_HOST'] = 'localhost'
# app.config['MYSQL_USER'] = 'root'
# app.config['MYSQL_PASSWORD'] = 'password'
# app.config['MYSQL_DB'] = 'ge'

# db_cursor = db.cursor()


app = Flask(__name__)

@app.route("/")
def login():
    return render_template("login.html", title = "login")

@app.route("/professor")
def professor():    
   return render_template("professor.html", title = "professor")

@app.route("/student")
def student():    
   return render_template("student.html", title = "student")

@app.route("/admin")
def admin():    
   return render_template("admin.html", title = "admin")

if __name__ == "__main__":
    app.run(debug = True)
