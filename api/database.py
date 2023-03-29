import sqlalchemy
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.dialects.mysql import BIGINT
from sqlalchemy import Column, text
from sqlalchemy.sql import func
from . import models
from datetime import datetime

engine = sqlalchemy.create_engine("mariadb+mariadbconnector://root:rdouda@localhost:3306/AttendanceSystem", echo=True)
Base = declarative_base()

class Student(Base):
    __tablename__ = 'students'
    uid = Column(sqlalchemy.Integer, primary_key=True)
    name = Column(sqlalchemy.String(length=128))
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
            name=student.name,
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
    existing_student.name = student.name
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
            'name': student.name,
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

def calculate_average_detections_by_email(start_date, end_date, start_time, end_time):
    start_datetime = datetime.combine(start_date, datetime.strptime(start_time, '%H:%M:%S').time())
    end_datetime = datetime.combine(end_date, datetime.strptime(end_time, '%H:%M:%S').time())
    results = []
    detections = (
        session.query(
            Detected.email,
            Detected.classroom,
            func.count(Detected.detection_id),
            func.min(Detected.detect_time),
            func.max(Detected.detect_time)
        )
        .filter(Detected.detect_time.between(start_datetime, end_datetime))
        .group_by(Detected.email, Detected.classroom)
        .all()
    )
    if not detections:
        return results
    
    for email, classroom, count, min_detect_time, max_detect_time in detections:
        detection_duration = (max_detect_time - min_detect_time).total_seconds()
        results.append({'email': email, 'detection_count': count, 'detection_duration': detection_duration, 'classroom': classroom}) 

    return results
