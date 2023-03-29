from . import database
from . import models
from pydantic import EmailStr
from fastapi import FastAPI
from datetime import date

app = FastAPI(title="Attendance System API", version='1.0')

@app.get('/')
async def index():
    return {'response': database.list_students()}

"""
    STUDENT MANAGEMENT
"""
@app.post('/add_student/', tags=['Student'])
async def add_student(student: models.Student):
    if database.add_student(student):
        return {'response': 'Student added.'}
    return {'response': 'Student already exists.'}

@app.post('/update_student/', tags=['Student'])
async def update_student(email: EmailStr, student: models.Student):
    if database.update_student(email, student):
        return {'response': 'Student updated.', 'student': student}
    return {'response': 'Student does not exists.'}


@app.post('/remove_student/', tags=['Student'])
async def remove_student(student_email: EmailStr):
    if database.remove_student(student_email):
        return {'response': 'Student removed.'}
    return {'response': 'Student does not exist.'}

@app.get('/list_students/', tags=['Student'])
async def list_students():
    return {'response': database.list_students()}

"""
    DETECTION
"""
@app.post('/add_detection/', tags=['Detection'])
async def add_detection(detected: models.Detection):
    database.add_detection(detected)
    return {'response': 'Added new detection.'}

@app.get('/list_detections/', tags=['Detection'])
async def get_detections():
    return {'response': database.list_detections()}

@app.post('/delete_detections/', tags=['Detection'])
async def delete_detections():
    database.delete_detections()
    return {'response': 'Deleted all detections.'}

"""
    UTILS
"""
@app.get("/average_detections_by_email", tags=['Utils'])
async def get_average_detections_by_email(start_date: date, end_date: date, start_time: str, end_time: str):
    return {'response': database.calculate_average_detections_by_email(start_date, end_date, start_time, end_time)}