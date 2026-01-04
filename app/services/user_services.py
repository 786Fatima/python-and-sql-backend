from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from sqlalchemy.sql import func
from app.models import User, Order, OrderItem, OrderStatus
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import hash_password

def create_user(db: Session, user: UserCreate):
    if len(user.password.encode("utf-8")) > 72:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password too long (max 72 bytes)"
        )

    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already exists"
        )

    if db.query(User).filter(User.mobile_number == user.mobileNumber).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Mobile number already exists"
        )

    hashed_password = hash_password(user.password)

    new_user = User(
        name=user.name,
        email=user.email,
        mobile_number=user.mobileNumber,
        hashed_password=hashed_password
    )

    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="User creation failed"
        )

def get_all_users(db: Session, skip: int = 0, limit: int = 10):
    return (
        db.query(User)
        .order_by(User.id)
        .offset(skip)
        .limit(limit)
        .all()
    )

def get_user_by_id(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user


def update_user(db: Session, user_id: int, data: UserUpdate):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # check email duplicacy
    if data.email and data.email != user.email:
        exists = db.query(User).filter(
            User.email == data.email,
            User.id != user_id
        ).first()
        if exists:
            raise HTTPException(409, "Email already exists")
        user.email = data.email

    # check mobile number duplicacy
    if data.mobileNumber:
        if data.mobileNumber != user.mobile_number:
            exists = db.query(User).filter(
                User.mobile_number == data.mobileNumber,
                User.id != user_id
            ).first()
            if exists:
                raise HTTPException(409, "Mobile number already exists")
            user.mobile_number = data.mobileNumber

    db.commit()
    db.refresh(user)
    return user

def delete_user(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    db.delete(user)
    db.commit()
    return {"message": "User deleted successfully"}

def top_users_by_spending(db: Session, limit: int = 10):
    result = (
        db.query(
            User.id.label("user_id"),
            User.name,
            User.email,
            func.sum(OrderItem.quantity * OrderItem.price)
            .label("total_spent")
        )
        .join(Order, Order.user_id == User.id)
        .join(OrderItem, OrderItem.order_id == Order.id)
        .filter(Order.status == OrderStatus.PAID)
        .group_by(User.id, User.name, User.email)
        .order_by(func.sum(OrderItem.quantity * OrderItem.price).desc())
        .limit(limit)
        .all()
    )

    return result