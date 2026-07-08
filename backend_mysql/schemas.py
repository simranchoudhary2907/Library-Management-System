from pydantic import BaseModel
from typing import List, Optional

class BookOut(BaseModel):
    id: int
    title: str
    author: Optional[str] = None
    category: Optional[str] = None
    available: Optional[int] = None

    class Config:
        orm_mode = True

class SeriesItem(BaseModel):
    month: str
    issued: int

class CategoryItem(BaseModel):
    name: str
    value: int

class Stats(BaseModel):
    series: List[SeriesItem]
    categories: List[CategoryItem]
