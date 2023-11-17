from pydantic import BaseModel, EmailStr
from datetime import datetime, date
from typing import Optional


class ChiffreBase(BaseModel):
    chiffre_affaire: int
    month: int
    year: int
    published: bool = True


class ChiffreCreate(ChiffreBase):
    pass


class UserOut(BaseModel):
    id: int
    email: EmailStr
    salon_name: str
    adresse: str
    region: str
    department: str
    open_date: date
    number_employees: int
    first_name: str
    last_name: str
    created_at: datetime

    class Config:
        orm_mode = True


class Chiffre(ChiffreBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut
    # ca_france: int

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    salon_name: str
    adresse: str
    region: str
    department: str
    open_date: date
    number_employees: int
    first_name: str
    last_name: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[int] = None
