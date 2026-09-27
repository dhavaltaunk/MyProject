import os
import httpx
from datetime import datetime
from typing import List

from models import NewsItem, Genre

NEWSAPI_KEY = os.getenv('NEWSAPI_KEY', '106c77c2cc6b4b368da3d977e509b948')
NEWSAPI_BASE_URL = 'https://newsapi.org/v2/everything'

# Cache storage
_cache = {
    'articles': [],
    'last_fetch': None,
    'genre_map': {'Finance': 'business', 'Sports': 'sports', 'Politics': 'politics', 'Science': 'science'}
}


async def fetch_news_from_newsapi() -> List[NewsItem]:
    """Fetch real news from NewsAPI for all genres"""
    articles = []
    genres: List[Genre] = ['Finance', 'Sports', 'Politics', 'Science']
    
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            for genre in genres:
                query = _cache['genre_map'].get(genre, genre.lower())
                params = {
                    'q': query,
                    'sortBy': 'publishedAt',
                    'apiKey': NEWSAPI_KEY,
                    'pageSize': 15,
                    'language': 'en'
                }
                
                response = await client.get(NEWSAPI_BASE_URL, params=params)
                response.raise_for_status()
                data = response.json()
                
                for article in data.get('articles', []):
                    try:
                        pub_date = datetime.fromisoformat(article['publishedAt'].replace('Z', '+00:00'))
                        
                        news_item = NewsItem(
                            id=article.get('url', ''),
                            title=article.get('title', '')[:100],
                            genre=genre,
                            summary=article.get('description', '')[:200],
                            source=article.get('source', {}).get('name', 'Unknown'),
                            date=pub_date,
                            url=article.get('url', '')
                        )
                        articles.append(news_item)
                    except Exception as e:
                        print(f'Error parsing article: {e}')
                        continue
    except httpx.HTTPError as e:
        print(f'NewsAPI request failed: {e}')
        if _cache['articles']:
            return _cache['articles']
        return []
    
    return articles


async def get_news_cached(max_age_minutes: int = 30) -> List[NewsItem]:
    """Get news from cache or fetch fresh if cache is stale"""
    now = datetime.now()
    
    if _cache['articles'] and _cache['last_fetch']:
        cache_age = (now - _cache['last_fetch']).total_seconds() / 60
        if cache_age < max_age_minutes:
            return _cache['articles']
    
    articles = await fetch_news_from_newsapi()
    _cache['articles'] = articles
    _cache['last_fetch'] = now
    
    return articles
