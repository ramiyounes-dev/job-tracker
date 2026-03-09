from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.auth import get_current_user
from app.database import get_db
from app.models import Application, User


router = APIRouter()

@router.get("/")
def get_status(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    result = db.query(Application.status, func.count()).filter(
        Application.user_id == current_user.id,
    ).group_by(Application.status).all()
    
    total = sum(count for _, count in result)
    
    result.append(("total", total))
    return dict(result)