from sqlalchemy import Column, Integer, String
from app.database import Base

class User(Base):
    __tablename__ = "Users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), index=True)
    email = Column(String(50), unique=True, index=True)
    mobile_number = Column(String(15), unique=True, index=True)
    hashed_password = Column(String(255), unique=True, index=True)
    created_at = Column(DateTime, server_default=func.now())
