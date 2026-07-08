from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from . import crud_raw, schemas

app = FastAPI(title='Library Management (MySQL raw)')
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/api/books', response_model=list[schemas.BookOut])
def books_list():
    return crud_raw.list_books()

@app.get('/api/stats', response_model=schemas.Stats)
def stats():
    return crud_raw.get_stats()

@app.post('/api/token')
def token():
    raise HTTPException(status_code=501, detail='Token endpoint not implemented in raw scaffold; see auth guide in README')
