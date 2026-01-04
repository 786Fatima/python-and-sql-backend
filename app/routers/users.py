from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List
from app.database import SessionLocal
from app.schemas.user import UserCreate, UserUpdate
from app.services.user_services import create_user, get_all_users, get_user_by_id, update_user, delete_user

router = APIRouter(prefix="/users", tags=["Users"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/register")
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    user = create_user(db, user)
    return {"message": "User registered successfully", "user": user}
 

@router.get("/get-all-users")
def list_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    return get_all_users(db, skip=skip, limit=limit)

@router.get("/get-user-by-id/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)):
    return get_user_by_id(db, user_id)


@router.put("/update-user/{user_id}")
def update_user_by_id(
    user_id: int,
    user: UserUpdate,
    db: Session = Depends(get_db)
):
    return update_user(db, user_id, user)

@router.delete("/delete-user/{user_id}")
def delete_user_by_id(user_id: int, db: Session = Depends(get_db)):
    return delete_user(db, user_id)
