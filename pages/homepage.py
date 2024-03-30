from flask import Flask, render_template, request, url_for
from flask_mysqldb import MySQL
# import MySQLdb.cursor      
import re
from attendance import detect_student
import os

# db_cursor = db.cursor()


app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'K09o4298!#lqsym'
app.config['MYSQL_DB'] = 'vision_attendance'
mysql = MySQL(app)


@app.route("/")
def login():
    return render_template("login.html", title = "login")

@app.route("/professor",  methods=['POST', 'GET'])
def professor(): 
   if request.method == "GET":
      id = detect_student()
      cursor = mysql.connection.cursor()
      cursor.execute(f"UPDATE attendance SET attended = attended + 1 WHERE student_id = {id}")
      mysql.connection.commit()
      cursor.close()
   return render_template("professor.html", title = "professor")

@app.route("/student")
def student():    
   return render_template("student.html", title = "student")

@app.route("/admin")
def admin():    
   return render_template("admin.html", title = "admin")

if __name__ == "__main__":
    app.run(debug = True)
