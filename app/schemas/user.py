from pydantic import BaseModel, Field, EmailStr, ConfigDict, validator
from typing import Optional
import phonenumbers


class UserBase(BaseModel):
    name: str = Field(..., min_length=3, max_length=100)
    email: EmailStr
    mobileNumber: str

    @validator('mobileNumber')
    def validate_mobile(cls, v):
        if v is None:
            return v 
        try:
            parsed = phonenumbers.parse(v, "IN")
            if not phonenumbers.is_possible_number(parsed):
                raise ValueError("Invalid phone number")

            return phonenumbers.format_number(parsed, None)
        except phonenumbers.NumberParseException:
            raise ValueError("Invalid phone number")


class UserCreate(UserBase): 
    password: str = Field(
        min_length=8,
        max_length=128,
        example="StrongPass@123"
    )


class UserUpdate(UserBase):
    pass  
