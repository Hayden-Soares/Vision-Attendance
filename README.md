# Vision Attendance
Vision attendance is a web application that takes attendance using face recognition. It was designed for universities and colleges to make the jobs of professors taking attendance easier. Now, all a student has to, is to is click a button while facing the camera and their attendance will be recorded.

The application features 3 users - 
- Student: Can view their attendance, but not modify anything.
- Professor: Can view attendance of their lectures, take attendance, and edit attendance of their lectures.
- Admin: Can view, edit and delete all attendances.

Moreover, the application features a **spoofing classifier** which can tell if a student is faking attendance by showing a photo of them or a real face. This is useful in a university environment where proxy attendance is common and it is difficult to implement electronic or biometric ID verification.

## Features
- Face recognition and matching implemented using **HOG object detection** in real time.
- **YOLO v8** used for implementation of spoofing classifier.
- Web application developed in **Flask** using **jinja2 templating engine**.
- Backend RDBMS implemented using **SQL**  and connected through mysql connector in python.

