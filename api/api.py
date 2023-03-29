from . import database
from .models import *

from fastapi import FastAPI
from datetime import date, datetime

app = FastAPI(title="Attendance System API", version='1.0')

@app.get('/')
async def index():
    return {'response': database.list_students()}

"""
    STUDENT MANAGEMENT
"""
@app.post('/add_student/', tags=['Student'])
async def add_student(student: StudentModel):
    if database.add_student(student):
        return {'response': 'SUCCESS', 'data':student.dict()}
    return {'response': 'FAILURE'}

@app.post('/update_student/', tags=['Student'])
async def update_student(email: EmailModel, student: StudentModel):
    if database.update_student(email, student):
        return {'response': 'SUCCESS', 'data': student.dict()}
    return {'response': 'FAILURE'}


@app.post('/remove_student/', tags=['Student'])
async def remove_student(student_email: EmailModel):
    if database.remove_student(student_email):
        return {'response': 'SUCCESS'}
    return {'response': 'FAILURE'}

@app.get('/list_students/', tags=['Student'])
async def list_students():
    return {'response': database.list_students()}

"""
    DETECTION
"""
@app.post('/add_detection/', tags=['Detection'])
async def add_detection(detected: DetectionModel):
    try:
        database.add_detection(detected)
    except Exception:
        return {'response': 'FAILURE'}
    return {'response': 'SUCCESS'}

@app.get('/list_detections/', tags=['Detection'])
async def get_detections():
    return {'response': database.list_detections()}

@app.post('/delete_detections/', tags=['Detection'])
async def delete_detections():
    database.delete_detections()
    return {'response': 'SUCCESS'}

"""
    UTILS
"""
@app.get("/average_detections_by_email", tags=['Utils'])
async def get_average_detections_by_email(start_date: date = date.today(), 
                                          end_date: date = date.today(), 
                                          start_time: str = datetime.now().strftime("%H:%M:%S"), 
                                          end_time: str = datetime.now().strftime("%H:%M:%S")):
    return {'response': database.calculate_average_detections_by_email(start_date, end_date, start_time, end_time)}