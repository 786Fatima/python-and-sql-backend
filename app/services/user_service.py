from sqlalchemy.orm import Session
from app.models.user import User

def create_user(
    db: Session,
    name: str,
    email: str,
    mobile_number: str,
    hashed_password: str
):
    try:
        user = User(
            name=name,
            email=email,
            mobile_number=mobile_number,
            hashed_password=hashed_password
        )

        db.add(user)
        db.commit()   # ONE commit
        db.refresh(user)

        return user

    # except IntegrityError:
    #     db.rollback()
    #     raise Exception("Email or mobile number already exists")

    except Exception as e:
        db.rollback()
        raise e


def fetch_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def fetch_all_users(db: Session):
    return db.query(User).all()