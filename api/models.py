from pydantic import BaseModel, Field, EmailStr

class StudentModel(BaseModel):
    name: str = Field(...)
    email: EmailStr = Field(...)

class DetectionModel(BaseModel):
    email: EmailStr = Field(...)
    classroom: int = Field(...)

class EmailModel(BaseModel):
    email: EmailStr = Field(...)