from config import db
import uuid, enum
from pgvector.sqlalchemy import Vector
from sqlalchemy import Enum


class UserType(str, enum.Enum):
    student = 'student'
    professor = 'professor'


class Users(db.Model):
    __tablename__ = 'users'

    user_id = db.Column(db.String, primary_key=True, default=str(uuid.uuid4()))
    email = db.Column(db.String, nullable=False, unique=True)
    user_type = db.Column(Enum(UserType), default=UserType.student, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    user_embedding = db.Column(Vector(512))
    completed_registration = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<User {self.email}>'
    
    def to_json(self):
        return {
            "userId": self.user_id,
            "email": self.email,
            "userType": self.user_type,
            "isAdmin": self.is_admin,
            "userEmbedding": self.user_embedding,
            "completedRegistration": self.completed_registration
        }


class Student(db.Model):
    __tablename__ = 'student'
    
    student_id = db.Column(db.String, primary_key=True, default=str(uuid.uuid4()))
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    roll_no = db.Column(db.String, nullable=False)
    class_id = db.Column(db.Integer, db.ForeignKey('class.class_id'))


    def __repr__(self):
        return f'<Student {self.first_name} {self.last_name}>'
    

    def to_json(self):
        return {
            "studentId": self.student_id,
            "firstName": self.first_name,
            "lastName": self.last_name,
            "rollNo": self.roll_no,
            "classId": self.class_id
        }
    

class Profs(db.Model):
    __tablename__ = 'profs'

    prof_id = db.Column(db.String, primary_key=True, default=str(uuid.uuid4()))
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f'<Prof {self.first_name} {self.last_name}>'
    
    def to_json(self):
        return {
            "profId": self.prof_id,
            "firstName": self.first_name,
            "lastName": self.last_name,
        }
    

class Class(db.Model):
    __tablename__ = 'class'

    class_id = db.Column(db.Integer, primary_key=True)
    class_rep = db.Column(db.String, db.ForeignKey('student.student_id'))
    faculty_advisor = db.Column(db.String, db.ForeignKey('profs.prof_id'))
    semester = db.Column(db.Integer, nullable=False)
    class_name = db.Column(db.String, nullable=False)
    class_description = db.Column(db.Text)

    def __repr__(self):
        return f'<Class {self.class_name}>'
    
    def to_json(self):
        return {
            "classId": self.class_id,
            "classRep": self.class_rep,
            "facultyAdvisor": self.faculty_advisor,
            "semester": self.semester,
            "className": self.class_name,
            "classDescription": self.class_description
        }



class Courses(db.Model):
    __tablename__ = 'courses'

    course_id = db.Column(db.String, primary_key=True)#uuid!
    course_code = db.Column(db.String, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    semester = db.Column(db.Integer, nullable=False)
    course_name = db.Column(db.String, nullable=False)
    course_description = db.Column(db.Text)
    taken_by = db.Column(db.String, db.ForeignKey('profs.prof_id'))
    classes_taken = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'<Course {self.course_name}>'
    
    def to_json(self):
        return {
            "courseId": self.course_id,
            "courseCode": self.course_code,
            "year": self.year,
            "semester": self.semester,
            "courseName": self.course_name,
            "courseDescription": self.course_description,
            "takenBy": self.taken_by,
            "classesTaken": self.classes_taken
        }

class Attendance(db.Model):
    __tablename__ = 'attendance'

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.String, db.ForeignKey('student.student_id'))
    attended = db.Column(db.Integer, nullable=False)
    course_id = db.Column(db.String, db.ForeignKey('courses.course_id'))

    def __repr__(self):
        return f'<Attendance {self.student_id} {self.course_id}>'
    
    def to_json(self):
        return {
            "id": self.id,
            "studentId": self.student_id,
            "attended": self.attended,
            "courseId": self.course_id,
        }
