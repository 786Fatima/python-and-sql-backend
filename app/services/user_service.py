from sqlalchemy.orm import Session
from app.models.user import User
from app.core.security import hash_password

def create_user(
    db: Session,
    name: str,
    email: str,
    mobile_number: str,
    password: str
):
    try:
        user = User(
            name=name,
            email=email,
            mobile_number=mobile_number,
            hashed_password=hash_password(password)
        )

        db.add(user)
        db.commit()  
        return user

    except Exception as e:
        db.rollback()
        raise e


def fetch_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def fetch_all_users(db: Session):
    return db.query(User).all()