from fastapi import FastAPI, HTTPException, Query, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional

from models import NewsItem, Genre
from data import get_news_cached, fetch_news_from_newsapi

app = FastAPI(title='News Aggregator API')

app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:5173', 'http://127.0.0.1:5173'],
    allow_methods=['GET', 'POST'],
    allow_headers=['*'],
)

@app.get('/news', response_model=List[NewsItem])
async def get_news(genre: Optional[Genre] = Query(None), q: Optional[str] = Query(None)):
    """Get news articles with optional genre and search filtering"""
    items = await get_news_cached()
    
    if genre:
        items = [item for item in items if item.genre == genre]
    
    if q:
        normalized = q.strip().lower()
        items = [
            item
            for item in items
            if normalized in item.title.lower() or normalized in item.summary.lower()
        ]
    
    return items

@app.get('/news/{news_id}', response_model=NewsItem)
async def get_news_item(news_id: str):
    """Get a single news item by URL"""
    items = await get_news_cached()
    for item in items:
        if item.id == news_id:
            return item
    raise HTTPException(status_code=404, detail='News item not found')

@app.get('/genres', response_model=List[Genre])
async def get_genres():
    """Get all available genres"""
    return ['Finance', 'Sports', 'Politics', 'Science']

@app.post('/news/refresh')
async def refresh_news(background_tasks: BackgroundTasks):
    """Manually trigger a refresh of all news articles"""
    background_tasks.add_task(fetch_news_from_newsapi)
    return {'status': 'refreshing', 'message': 'News refresh started in background'}
