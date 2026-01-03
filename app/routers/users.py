from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.services.user_service import create_user, fetch_user_by_email, fetch_all_users

router = APIRouter(prefix="/users", tags=["Users"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/register-user")
def register_user(name: str, email: str, mobile_number: str, hashed_password: str, db: Session = Depends(get_db)):
    user = create_user(db, name, email, mobile_number, hashed_password)
    return {"message": "User registered successfully", "user": user}

@router.get("/get-user-by-email")
def get_user_by_email(email: str, db: Session = Depends(get_db)):
    user = get_user_by_email(db, email)
    return {"user": user}   

@router.get("/get-all-users")
def get_all_users(db: Session = Depends(get_db)):
    users = fetch_all_users(db)
    return {"users": users}