from flask import Flask, render_template, request, url_for
from flask_mysqldb import MySQL
# import MySQLdb.cursor      
import re
from attendance import detect_student


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
   if request.method == "POST":
      id = detect_student()
      cursor = mysql.connection.cursor()
      cursor.execute(f"UPDATE attendance SET attended = attended + 1 WHERE student_id = {id}")
      mysql.connection.commit()
      cursor.close()
   return render_template("professor.html", title = "professor")

@app.route("/student")
def student(): 
   cursor = mysql.connection.cursor()
   cursor.execute('SELECT c.course_code, c.course_name, (a.attended) * 100.0 / c.classes_taken '
   + 'AS attendance_percentage '
   + 'FROM courses c '
   + 'JOIN attendance a ON c.course_code = a.course_id '
   + 'JOIN student s ON a.student_id = s.id '
   + 'JOIN classes cl ON s.class_id = cl.class_id '
   + 'WHERE s.id = 4738 '
   + 'AND c.semester = cl.semester')
   get = cursor.fetchall()
   get2 = [None] * len(get) 
   for i in range(len(get)):
      get2[i] = (get[i][0], get[i][1], round(get[i][2]))
   mysql.connection.commit()
   cursor.close()
   return render_template("student.html", title = "student", get = get2)

@app.route("/s3425")
def s3425(): 
   cursor = mysql.connection.cursor()
   cursor.execute('SELECT c.course_code, c.course_name, (a.attended) * 100.0 / c.classes_taken '
   + 'AS attendance_percentage '
   + 'FROM courses c '
   + 'JOIN attendance a ON c.course_code = a.course_id '
   + 'JOIN student s ON a.student_id = s.id '
   + 'JOIN classes cl ON s.class_id = cl.class_id '
   + 'WHERE s.id = 3425 '
   + 'AND c.semester = cl.semester')
   get = cursor.fetchall()
   mysql.connection.commit()
   cursor.close()
   return render_template("student.html", title = "student", get = get)

@app.route("/s4884")
def s4884(): 
   cursor = mysql.connection.cursor()
   cursor.execute('SELECT c.course_code, c.course_name, (a.attended) * 100.0 / c.classes_taken '
   + 'AS attendance_percentage '
   + 'FROM courses c '
   + 'JOIN attendance a ON c.course_code = a.course_id '
   + 'JOIN student s ON a.student_id = s.id '
   + 'JOIN classes cl ON s.class_id = cl.class_id '
   + 'WHERE s.id = 4884 '
   + 'AND c.semester = cl.semester')
   get = cursor.fetchall()
   mysql.connection.commit()
   cursor.close()
   return render_template("student.html", title = "student", get = get)

@app.route("/s7734")
def s7734(): 
   cursor = mysql.connection.cursor()
   cursor.execute('SELECT c.course_code, c.course_name, (a.attended) * 100.0 / c.classes_taken '
   + 'AS attendance_percentage '
   + 'FROM courses c '
   + 'JOIN attendance a ON c.course_code = a.course_id '
   + 'JOIN student s ON a.student_id = s.id '
   + 'JOIN classes cl ON s.class_id = cl.class_id '
   + 'WHERE s.id = 7734 '
   + 'AND c.semester = cl.semester')
   get = cursor.fetchall()
   mysql.connection.commit()
   cursor.close()
   return render_template("student.html", title = "student", get = get)

@app.route("/s9201")
def s9201(): 
   cursor = mysql.connection.cursor()
   cursor.execute('SELECT c.course_code, c.course_name, (a.attended) * 100.0 / c.classes_taken '
   + 'AS attendance_percentage '
   + 'FROM courses c '
   + 'JOIN attendance a ON c.course_code = a.course_id '
   + 'JOIN student s ON a.student_id = s.id '
   + 'JOIN classes cl ON s.class_id = cl.class_id '
   + 'WHERE s.id = 9201 '
   + 'AND c.semester = cl.semester')
   get = cursor.fetchall()
   mysql.connection.commit()
   cursor.close()
   return render_template("student.html", title = "student", get = get)

@app.route("/s1001")
def s1001(): 
   cursor = mysql.connection.cursor()
   cursor.execute('SELECT c.course_code, c.course_name, (a.attended) * 100.0 / c.classes_taken '
   + 'AS attendance_percentage '
   + 'FROM courses c '
   + 'JOIN attendance a ON c.course_code = a.course_id '
   + 'JOIN student s ON a.student_id = s.id '
   + 'JOIN classes cl ON s.class_id = cl.class_id '
   + 'WHERE s.id = 1001 '
   + 'AND c.semester = cl.semester')
   get = cursor.fetchall()
   mysql.connection.commit()
   cursor.close()
   return render_template("student.html", title = "student", get = get)

@app.route("/admin")
def admin():    
   return render_template("admin.html", title = "admin")

if __name__ == "__main__":
    app.run(debug = True)
