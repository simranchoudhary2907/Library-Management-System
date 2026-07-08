from datetime import date, timedelta
from sqlalchemy.orm import Session
from .auth_utils import get_password_hash, verify_password
from . import models, schemas


def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def authenticate_user(db: Session, username: str, password: str):
    user = get_user_by_username(db, username)
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user


def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(
        username=user.username,
        hashed_password=hashed_password,
        role=user.role,
        member_id=user.member_id,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_all_users(db: Session):
    return db.query(models.User).all()


def create_member(db: Session, member: schemas.MemberCreate):
    db_member = models.Member(
        member_id=member.member_id,
        name=member.name,
        email=member.email,
        phone=member.phone,
    )
    db.add(db_member)
    db.commit()
    db.refresh(db_member)
    return db_member


def get_member_by_id(db: Session, member_id: str):
    return db.query(models.Member).filter(models.Member.member_id == member_id).first()


def get_all_members(db: Session):
    return db.query(models.Member).all()


def update_member(db: Session, member_id: str, member: schemas.MemberCreate):
    db_member = get_member_by_id(db, member_id)
    if not db_member:
        return None
    db_member.name = member.name
    db_member.email = member.email
    db_member.phone = member.phone
    db.commit()
    db.refresh(db_member)
    return db_member


def delete_member(db: Session, member_id: str):
    db_member = get_member_by_id(db, member_id)
    if not db_member:
        return None
    db.delete(db_member)
    db.commit()
    return db_member


def get_book_by_id(db: Session, book_id: str):
    return db.query(models.Book).filter(models.Book.book_id == book_id).first()


def get_all_books(db: Session):
    return db.query(models.Book).all()


def create_book(db: Session, book: schemas.BookCreate):
    availability = "Available" if book.quantity > 0 else "Not Available"
    db_book = models.Book(
        book_id=book.book_id,
        title=book.title,
        author=book.author,
        genre=book.genre,
        quantity=book.quantity,
        availability=availability,
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


def update_book(db: Session, book_id: str, book: schemas.BookCreate):
    db_book = get_book_by_id(db, book_id)
    if not db_book:
        return None
    db_book.title = book.title
    db_book.author = book.author
    db_book.genre = book.genre
    db_book.quantity = book.quantity
    db_book.availability = "Available" if book.quantity > 0 else "Not Available"
    db.commit()
    db.refresh(db_book)
    return db_book


def delete_book(db: Session, book_id: str):
    db_book = get_book_by_id(db, book_id)
    if not db_book:
        return None
    db.delete(db_book)
    db.commit()
    return db_book


def issue_book(db: Session, record: schemas.BorrowRecordCreate):
    book = get_book_by_id(db, record.book_id)
    member = get_member_by_id(db, record.member_id)
    if not book or book.quantity <= 0 or not member:
        return None

    book.quantity -= 1
    book.availability = "Available" if book.quantity > 0 else "Not Available"

    borrow_date = date.today()
    due_date = borrow_date + timedelta(days=7)

    db_record = models.BorrowRecord(
        member_id=record.member_id,
        book_id=record.book_id,
        borrow_date=borrow_date,
        due_date=due_date,
        status="Borrowed",
    )
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    return db_record


def return_book(db: Session, record: schemas.BorrowRecordCreate):
    borrow_record = db.query(models.BorrowRecord).filter(
        models.BorrowRecord.member_id == record.member_id,
        models.BorrowRecord.book_id == record.book_id,
        models.BorrowRecord.status == "Borrowed",
    ).first()
    if not borrow_record:
        return None

    borrow_record.status = "Returned"

    book = get_book_by_id(db, record.book_id)
    if book:
        book.quantity += 1
        book.availability = "Available"

    db.commit()
    db.refresh(borrow_record)
    return borrow_record


def get_borrow_records(db: Session):
    return db.query(models.BorrowRecord).all()


def get_overdue_records(db: Session):
    today = date.today()
    return db.query(models.BorrowRecord).filter(
        models.BorrowRecord.status == "Borrowed",
        models.BorrowRecord.due_date < today,
    ).all()
