from pydantic import BaseModel, Field, EmailStr

class Student(BaseModel):
    first_name: str = Field(...)
    last_name: str = Field(...)
    email: EmailStr = Field(...)

class Detection(BaseModel):
    email: EmailStr = Field(...)
    classroom: int = Field(...)