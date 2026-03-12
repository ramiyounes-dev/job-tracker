from pydantic import BaseModel
from pydantic import ConfigDict
from datetime import datetime

class UserCreate(BaseModel):
    email: str
    password: str

class UserUpdate(BaseModel):
    email: str | None = None
    password: str | None = None

class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    email: str
    created_at: datetime

class ApplicationCreate(BaseModel):
    company_name: str
    job_title: str
    location: str
    status: str
    job_url: str | None = None
    notes: str | None = None

class ApplicationUpdate(BaseModel):
    company_name: str | None = None
    job_title: str | None = None
    location: str | None = None
    status: str | None = None
    job_url: str | None = None
    notes: str | None = None

class ApplicationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    user_id: int
    company_name: str
    job_title: str
    location: str
    status: str
    job_url: str | None = None
    notes: str | None = None
    applied_at: datetime
    updated_at: datetime
    
class ContactCreate(BaseModel):
    name: str
    email: str
    phone: str | None = None
    role: str | None = None

class ContactUpdate(BaseModel):
    name: str | None = None
    email: str | None = None
    phone: str | None = None
    role: str | None = None

class ContactResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    application_id: int
    name: str
    email: str
    phone: str | None = None
    role: str | None = None
    created_at: datetime