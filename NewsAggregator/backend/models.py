from datetime import datetime
from pydantic import BaseModel, HttpUrl
from typing import Literal

Genre = Literal['Finance', 'Sports', 'Politics', 'Science']

class NewsItem(BaseModel):
    id: str
    title: str
    genre: Genre
    summary: str
    source: str
    date: datetime
    url: HttpUrl
