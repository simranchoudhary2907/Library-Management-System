from datetime import date
from typing import Optional
from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    username: str
    role: str


class UserCreate(UserBase):
    password: str
    member_id: Optional[str] = None


class UserOut(UserBase):
    id: int
    member_id: Optional[str] = None

    class Config:
        orm_mode = True


class MemberBase(BaseModel):
    member_id: str
    name: str
    email: EmailStr
    phone: str


class MemberCreate(MemberBase):
    pass


class MemberOut(MemberBase):
    id: int

    class Config:
        orm_mode = True


class BookBase(BaseModel):
    book_id: str
    title: str
    author: str
    genre: str
    quantity: int


class BookCreate(BookBase):
    pass


class BookOut(BookBase):
    id: int
    availability: str

    class Config:
        orm_mode = True


class BorrowRecordBase(BaseModel):
    member_id: str
    book_id: str


class BorrowRecordCreate(BorrowRecordBase):
    pass


class BorrowRecordOut(BorrowRecordBase):
    id: int
    borrow_date: date
    due_date: date
    status: str

    class Config:
        orm_mode = True
