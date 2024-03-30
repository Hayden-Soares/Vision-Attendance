import mysql.connector


db = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="password",
    database="vision_attendance"
)
#db_cursor = db.cursor()

# ^ I believe this bit should be run once only, when launching website(?)


def update_student_attendance(db, id, course):
    #course = course code, which is a primary key integer
    #id = student id
    #run this when the student face is detected and the ID is output

    db_cursor = db.cursor()
    update_att_query = (
        'UPDATE attendance '
        'SET attended = attended + 1 '
        'WHERE course_id = %s '
        'AND student_id = %s;'
    )
    db_cursor.execute(update_att_query, [course, id])
    db.commit()


def make_new_course(db, code, class_id, name, prof_id, sem):
    # int, int, string, int, int
    # Initializes the course by adding new course and attendance values for students in the course
    # Professor should run this at the start of the sem

    db_cursor = db.cursor()

    insert_course_query = (
        'INSERT INTO courses (course_code, course_class, course_name, taken_by, semester, classes_taken) '
        'VALUES (%s, %s, %s, %s, %s, 0)'
    )
    db_cursor.execute(insert_course_query, [code, class_id, name, prof_id, sem])

    insert_attendance_query = (
        'INSERT INTO attendance (course_id, student_id, attended) '
        'SELECT %s, s.id, 0 '
        'FROM student s '
        'JOIN classes cl ON s.class_id = cl.class_id '
        'WHERE cl.class_id = %s'
    )
    db_cursor.execute(insert_attendance_query, [code, class_id])
    db.commit()


def start_class(db, course_code):
    # run this when the button to launch the CV window
    # Increments classes taken by one

    db_cursor = db.cursor()

    start_class_query = (
    'UPDATE courses '
    'SET classes_taken = classes_taken + 1 '
    'WHERE course_code = %s;'
    )
    db_cursor.execute(start_class_query, [course_code])
    db.commit()


def get_attendance_percentages(db, student_id):
    # returns attendance percentages of a particular student in all classes of their current semester
    # returns a list of [course code, course name, percentage]

    db_cursor = db.cursor()
    get_att_query = (
        'SELECT c.course_code, c.course_name, (a.attended) * 100.0 / c.classes_taken '
        'AS attendance_percentage '
        'FROM courses c '
        'JOIN attendance a ON c.course_code = a.course_id '
        'JOIN student s ON a.student_id = s.id '
        'JOIN classes cl ON s.class_id = cl.class_id '
        'WHERE s.id = %s '
        'AND c.semester = cl.semester'
    )

    db_cursor.execute(get_att_query, [student_id])
    attendances = db_cursor.fetchall()
    for x in attendances:
        x = list(x)
        x[2] = float(x[2])
        #print(x)

    return attendances


def get_all_attendance(db, course_id):
    #returns [studentid, Name, percentage] for all students in a course


    db_cursor = db.cursor()
    get_all = (
        'SELECT s.id, '
        'CONCAT(s.first_name, \' \', s.last_name) AS name, '
        '(a.attended * 100.0 / c.classes_taken) AS attendance_percentage '
        'FROM student s '
        'JOIN attendance a ON s.id = a.student_id '
        'JOIN courses c ON a.course_id = c.course_code '
        'WHERE c.course_code = %s;'
    )
    db_cursor.execute(get_all, [course_id])
    ats = db_cursor.fetchall()
    attendances = []
    for x in ats:
        attendances.append(list(x))
        attendances[-1][2] = float(attendances[-1][2])

    return attendances
    #for x in attendances:
    #    print(x)


def get_login(db, username, password):
    # returns [prof or student, their prof/student ID]
    # 0 -> student
    # 1 -> prof
    db_cursor = db.cursor()
    db_cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", [username, password])
    user = db_cursor.fetchone()  # Fetch the first result

    if user == None:
        return [-1, -1, -1]

    if user[3] == 'student':
        db_cursor.execute("SELECT * FROM student_user_map WHERE user_id = %s", [user[0]])
        s = db_cursor.fetchone()
        db_cursor.execute(
            "SELECT CONCAT(first_name, \' \', last_name) AS name from student "
            "WHERE id = %s", [s[0]])
        name = db_cursor.fetchone()
        st = [0, s[0], name[0]]
        return st
    
    else:
        db_cursor.execute("SELECT * FROM prof_user_map WHERE user_id = %s", [user[0]])
        p = db_cursor.fetchone()
        db_cursor.execute(
            "SELECT CONCAT(first_name, \' \', last_name) AS name from profs "
            "WHERE id = %s", [p[0]])
        name = db_cursor.fetchone()
        pr = [1, p[0], name[0]]
        return pr
    
def get_all_courses(db, prof_id):
    db_cursor = db.cursor()
    db_cursor.execute("SELECT course_code, course_name FROM courses WHERE taken_by = %s", [prof_id])
    c = db_cursor.fetchall()
    return c


#make_new_course(256, 227, "Computer architecture and organization", 2, 4)
#start_class(256)
#update_student_attendance(4884, 256)
#update_student_attendance(4884, 254)
#get_all_attendance(db, 254)






#db.commit()
# ^ This needs to be run after an update query, it updates the database.