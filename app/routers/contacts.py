
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.auth import get_current_user
from app.database import get_db
from app.models import Application, Contact, User
from app.schemas import ContactCreate, ContactResponse, ContactUpdate


router = APIRouter()

def verify_application_ownership(db, app_id, current_user):
    application = db.query(Application).filter(
    Application.id == app_id,
    Application.user_id == current_user.id).first()
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")

@router.post("/{app_id}/contacts", response_model=ContactResponse)
def create_contact(app_id: int, contact: ContactCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    verify_application_ownership(db, app_id, current_user)
    new_contact = Contact(
        application_id=app_id,
        name =contact.name,
        email=contact.email,
        phone=contact.phone,
        role=contact.role
    )
    db.add(new_contact)
    db.commit()
    db.refresh(new_contact)
    return ContactResponse.model_validate(new_contact)

@router.get("/{app_id}/contacts/{contact_id}", response_model=ContactResponse)
def get_contact(app_id: int, contact_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    verify_application_ownership(db, app_id, current_user)
    contact = db.query(Contact).filter(Contact.application_id == app_id).filter(Contact.id == contact_id).first()
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    return ContactResponse.model_validate(contact)

@router.get("/{app_id}/contacts", response_model=list[ContactResponse])
def get_contacts(app_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    verify_application_ownership(db, app_id, current_user)
    contacts = db.query(Contact).filter(Contact.application_id == app_id).all()
    if not contacts:
        return []
    return [ContactResponse.model_validate(c) for c in contacts]

@router.put("/{app_id}/contacts/{contact_id}", response_model=ContactResponse)
def update_contact(app_id: int, contact_id: int, contact_update: ContactUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    verify_application_ownership(db, app_id, current_user)
    contact = db.query(Contact).filter(Contact.id == contact_id).filter(Contact.application_id == app_id).first()
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    for key, value in contact_update.model_dump(exclude_unset=True).items():
        setattr(contact, key, value)
    db.commit()
    db.refresh(contact)
    return ContactResponse.model_validate(contact)

@router.delete("/{app_id}/contacts/{contact_id}", status_code=204)
def delete_contact(app_id: int, contact_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    verify_application_ownership(db, app_id, current_user)
    contact = db.query(Contact).filter(Contact.id == contact_id).filter(Contact.application_id == app_id).first()
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    db.delete(contact)
    db.commit()
    return None