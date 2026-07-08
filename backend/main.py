from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from . import crud, models, schemas
from .database import SessionLocal, engine
from .auth_utils import create_access_token, verify_token

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Library Management System API")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token", auto_error=False)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    payload = verify_token(token)
    if not payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    username = payload.get("sub")
    if username is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    user = crud.get_user_by_username(db, username)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    return user


def get_optional_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    if not token:
        return None
    payload = verify_token(token)
    if not payload:
        return None
    username = payload.get("sub")
    if username is None:
        return None
    return crud.get_user_by_username(db, username)


def require_admin(user: models.User = Depends(get_current_user)):
    if user.role != "Admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin privileges required")
    return user


@app.post("/token")
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
    access_token = create_access_token(data={"sub": user.username, "role": user.role})
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/users/me", response_model=schemas.UserOut)
def read_current_user(current_user: models.User = Depends(get_current_user)):
    return current_user


@app.get("/users/", response_model=list[schemas.UserOut])
def read_users(db: Session = Depends(get_db), _: models.User = Depends(require_admin)):
    return crud.get_all_users(db)


@app.post("/users/", response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db), current_user: models.User | None = Depends(get_optional_current_user)):
    existing_users = db.query(models.User).count()
    if existing_users > 0 and (current_user is None or current_user.role != "Admin"):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin privileges required to add users")
    if crud.get_user_by_username(db, user.username):
        raise HTTPException(status_code=400, detail="Username already registered")
    if user.member_id and not crud.get_member_by_id(db, user.member_id):
        raise HTTPException(status_code=400, detail="Member record not found for the specified member_id")
    return crud.create_user(db, user)


@app.post("/members/", response_model=schemas.MemberOut)
def create_member(member: schemas.MemberCreate, db: Session = Depends(get_db)):
    if crud.get_member_by_id(db, member.member_id):
        raise HTTPException(status_code=400, detail="Member ID already exists")
    return crud.create_member(db, member)


@app.get("/members/", response_model=list[schemas.MemberOut])
def read_members(db: Session = Depends(get_db), _: models.User = Depends(require_admin)):
    return crud.get_all_members(db)


@app.get("/members/{member_id}", response_model=schemas.MemberOut)
def read_member(member_id: str, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    if current_user.role != "Admin" and current_user.member_id != member_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    db_member = crud.get_member_by_id(db, member_id)
    if db_member is None:
        raise HTTPException(status_code=404, detail="Member not found")
    return db_member


@app.put("/members/{member_id}", response_model=schemas.MemberOut)
def update_member(member_id: str, member: schemas.MemberCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    if current_user.role != "Admin" and current_user.member_id != member_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    updated = crud.update_member(db, member_id, member)
    if updated is None:
        raise HTTPException(status_code=404, detail="Member not found")
    return updated


@app.delete("/members/{member_id}", response_model=schemas.MemberOut)
def delete_member(member_id: str, db: Session = Depends(get_db), _: models.User = Depends(require_admin)):
    deleted = crud.delete_member(db, member_id)
    if deleted is None:
        raise HTTPException(status_code=404, detail="Member not found")
    return deleted


@app.post("/books/", response_model=schemas.BookOut)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db), _: models.User = Depends(require_admin)):
    if crud.get_book_by_id(db, book.book_id):
        raise HTTPException(status_code=400, detail="Book ID already exists")
    return crud.create_book(db, book)


@app.get("/books/", response_model=list[schemas.BookOut])
def read_books(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_all_books(db)[skip : skip + limit]


@app.get("/books/{book_id}", response_model=schemas.BookOut)
def read_book(book_id: str, db: Session = Depends(get_db)):
    db_book = crud.get_book_by_id(db, book_id)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book


@app.put("/books/{book_id}", response_model=schemas.BookOut)
def update_book(book_id: str, book: schemas.BookCreate, db: Session = Depends(get_db), _: models.User = Depends(require_admin)):
    updated = crud.update_book(db, book_id, book)
    if updated is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return updated


@app.delete("/books/{book_id}", response_model=schemas.BookOut)
def delete_book(book_id: str, db: Session = Depends(get_db), _: models.User = Depends(require_admin)):
    deleted = crud.delete_book(db, book_id)
    if deleted is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return deleted


@app.post("/borrow/", response_model=schemas.BorrowRecordOut)
def issue_book(record: schemas.BorrowRecordCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    if current_user.role != "Admin" and current_user.member_id != record.member_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to issue for this member")
    borrow_record = crud.issue_book(db, record)
    if not borrow_record:
        raise HTTPException(status_code=400, detail="Book unavailable, member not found, or book does not exist")
    return borrow_record


@app.post("/return/", response_model=schemas.BorrowRecordOut)
def return_book(record: schemas.BorrowRecordCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    if current_user.role != "Admin" and current_user.member_id != record.member_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to return for this member")
    borrow_record = crud.return_book(db, record)
    if not borrow_record:
        raise HTTPException(status_code=400, detail="Borrow record not found")
    return borrow_record


@app.get("/borrow_records/", response_model=list[schemas.BorrowRecordOut])
def read_borrow_records(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    if current_user.role == "Admin":
        return crud.get_borrow_records(db)
    return db.query(models.BorrowRecord).filter(models.BorrowRecord.member_id == current_user.member_id).all()


@app.get("/overdue/", response_model=list[schemas.BorrowRecordOut])
def read_overdue(db: Session = Depends(get_db), current_user: models.User = Depends(require_admin)):
    return crud.get_overdue_records(db)
