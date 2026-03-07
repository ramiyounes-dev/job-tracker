
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.auth import get_current_user
from app.database import get_db
from app.models import Application, User
from app.schemas import ApplicationCreate, ApplicationResponse, ApplicationUpdate


router = APIRouter()

@router.post("/", response_model=ApplicationResponse)
def create_application(application: ApplicationCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    new_application = Application(
        user_id=current_user.id,
        company_name=application.company_name,
        job_title=application.job_title,
        location=application.location,
        status=application.status,
        job_url=application.job_url,
        notes=application.notes
    )
    db.add(new_application)
    db.commit()
    db.refresh(new_application)
    return ApplicationResponse.model_validate(new_application)

@router.get("/{application_id}",response_model=ApplicationResponse)
def get_application(application_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    application = db.query(Application).filter(Application.id == application_id).filter(Application.user_id == current_user.id).first()
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    return ApplicationResponse.model_validate(application)



@router.get("/", response_model=list[ApplicationResponse])
def get_applications(status: str = None, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    applications = db.query(Application).filter(Application.user_id == current_user.id)
    if not applications:
        return []
    if status:
        applications = applications.filter(Application.status == status)
    applications =  applications.all()
    return [ApplicationResponse.model_validate(app) for app in applications]

@router.delete("/{application_id}", status_code=204)
def delete_application(application_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    application = db.query(Application).filter(Application.id == application_id).filter(Application.user_id == current_user.id).first()
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    db.delete(application)
    db.commit()
    return None

@router.put("/{application_id}", response_model=ApplicationResponse)
def update_application(application_id: int, application_update: ApplicationUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    application = db.query(Application).filter(Application.id == application_id).filter(Application.user_id == current_user.id).first()
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    
    for key, value in application_update.model_dump(exclude_unset=True).items():
        setattr(application, key, value)
    
    db.commit()
    db.refresh(application)
    return ApplicationResponse.model_validate(application)  