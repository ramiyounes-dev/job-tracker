from fastapi import FastAPI
from app.models import User, Application, Contact
from app.database import engine, Base
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup code: create database tables
    Base.metadata.create_all(bind=engine)
    yield
    # Shutdown code 

app = FastAPI(
    title="Job Application Tracker API",
    description="A simple API to track job applications, contacts, and user accounts.",
    version="1.0.0",
    lifespan=lifespan
)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Job Application Tracker API!"}