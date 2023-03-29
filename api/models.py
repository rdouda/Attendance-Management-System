from pydantic import BaseModel, Field, EmailStr

class Student(BaseModel):
    name: str = Field(...)
    email: EmailStr = Field(...)

class Detection(BaseModel):
    email: EmailStr = Field(...)
    classroom: int = Field(...)