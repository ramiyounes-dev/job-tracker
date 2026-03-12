from app.database import Base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)

    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    applications = relationship("Application", backref="user", cascade="all, delete-orphan")

class Application(Base):
    __tablename__ = "applications"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"),  nullable=False)

    company_name = Column(String, nullable=False)
    job_title = Column(String, nullable=False)
    location = Column(String, nullable=False)
    status = Column(String, nullable=False)
    applied_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    job_url = Column(String, nullable=True)
    notes = Column(String, nullable=True)

    contacts = relationship("Contact", backref="application", cascade="all, delete-orphan")
    
class Contact(Base):
    __tablename__ = "contacts"
    id = Column(Integer, primary_key=True, index=True)
    application_id = Column(Integer, ForeignKey("applications.id"), nullable=False)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    phone = Column(String, nullable=True)
    role = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
