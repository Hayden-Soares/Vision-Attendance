import mysql.connector


db = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="password",
    database="vision_attendance"
)
db_cursor = db.cursor()

# ^ I believe this bit should be run once only, when launching website(?)


def update_student_attendance(id, course):
    #course = course code, which is a primary key integer
    #id = student id
    #run this when the student face is detected and the ID is output


    update_att_query = (
        'UPDATE attendance '
        'SET attended = attended + 1 '
        'WHERE course_id = %s '
        'AND student_id = %s;'
    )
    db_cursor.execute(update_att_query, [course, id])


def make_new_course(code, class_id, name, prof_id, sem):
    # int, int, string, int, int
    # Initializes the course by adding new course and attendance values for students in the course
    # Professor should run this at the start of the sem

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



def start_class(course_code):
    # run this when the button to launch the CV window
    # Increments classes taken by one

    start_class_query = (
    'UPDATE courses '
    'SET classes_taken = classes_taken + 1 '
    'WHERE course_code = %s;'
    )
    db_cursor.execute(start_class_query, [course_code])

def get_attendance_percentages(student_id):
    # returns attendance percentages of a particular student in all classes of their current semester
    # returns a dict of {course_id: percentage}

    get_att_query = (
        'SELECT c.course_code, (a.attended) * 100.0 / c.classes_taken '
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
    attendance_dict = {}
    for x in attendances:
        attendance_dict[x[0]] = x[1]

    #for (k, v) in attendance_dict.items():
    #    print(k, v)
    
    return attendance_dict

    
#make_new_course(256, 227, "Computer architecture and organization", 2, 4)
#start_class(256)
#update_student_attendance(4884, 256)
#update_student_attendance(4884, 254)
#get_attendance_percentages(4884)


db.commit()
# ^ This needs to be run after an update query, it updates the database.