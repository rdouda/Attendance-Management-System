import sqlalchemy
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.dialects.mysql import BIGINT
from sqlalchemy import Column, text
from sqlalchemy.sql import func
from . import models
from . import utils
from datetime import datetime, time

engine = sqlalchemy.create_engine("mariadb+mariadbconnector://root:rdouda@localhost:3306/AttendanceSystem", echo=True)
Base = declarative_base()

class Student(Base):
    __tablename__ = 'students'
    uid = Column(sqlalchemy.Integer, primary_key=True)
    first_name = Column(sqlalchemy.String(length=128))
    last_name = Column(sqlalchemy.String(length=128))
    email = Column(sqlalchemy.String(length=128), unique=True)

class Detected(Base):
    __tablename__ = 'detected'
    detection_id = Column(BIGINT(unsigned=True), primary_key=True)
    email = Column(sqlalchemy.String(length=128))
    detect_time = Column(sqlalchemy.DateTime, default=func.now())
    classroom = Column(sqlalchemy.Integer)

#Base.metadata.drop_all(engine)
#Base.metadata.create_all(engine)

Session = sessionmaker(engine)
Session.configure(bind=engine)
session = Session()


"""
    STUDENT MANAGEMENT
"""
def add_student(student: models.Student):
    existing_student = session.query(Student).filter_by(email=student.email.lower()).first()
    if existing_student:
        return False
    else:
        new_student = Student(
            first_name=student.first_name,
            last_name=student.last_name,
            email=student.email,
        )
        session.add(new_student)
        session.commit()
        return True

def update_student(email, student: models.Student):
    existing_student = session.query(Student).filter_by(email=email.lower()).first()
    if existing_student is None:
        return False
    existing_student.email = student.email
    existing_student.first_name = student.first_name
    existing_student.last_name = student.last_name
    session.commit()
    return True

def remove_student(student_email):
    deleted = session.query(Student).filter(Student.email == student_email.lower()).delete()
    session.commit()
    if deleted > 0:
        return True
    return False

def list_students():
    students = session.query(Student).all()
    students_list = []
    for student in students:
        student_dict = {
            'uid': student.uid,
            'first_name': student.first_name,
            'last_name': student.last_name,
            'email': student.email,
        }
        students_list.append(student_dict)
    return {'students': students_list}

"""
    DETECTION
"""
def add_detection(detected: models.Detection):
    new_detection = Detected(email=detected.email, classroom=detected.classroom)
    session.add(new_detection)
    session.commit()

def list_detections():
    detections = session.query(Detected).all()
    detections_list = []
    for detection in detections:
        detection_dict = {
            'detection_id': detection.detection_id,
            'date': detection.detect_time,
            'detected_email': detection.email,
            'classroom': detection.classroom
        }
        detections_list.append(detection_dict)
    return detections_list

def delete_detections():
    session.query(Detected).delete()
    session.commit()
    session.execute(text('ALTER TABLE detected AUTO_INCREMENT = 1'))
    session.commit()

def calculate_average_detections_by_email(email, start_date, end_date, start_time, end_time, classroom: int):
    start_datetime = datetime.combine(start_date, datetime.strptime(start_time, '%H:%M:%S').time())
    end_datetime = datetime.combine(end_date, datetime.strptime(end_time, '%H:%M:%S').time())
    total_duration = (end_datetime - start_datetime).total_seconds()
    detections = (
        session.query(
            Detected.email,
            func.count(Detected.detection_id)
        )
        .filter(email.lower() == Detected.email, classroom == Detected.classroom, Detected.detect_time.between(start_datetime, end_datetime))
        .all()
    )
    if detections is None:
        return 0
    count = detections[0][1]
    detection_duration = count / total_duration
    detection_percentage = detection_duration * 100

    return {email: detection_percentage}