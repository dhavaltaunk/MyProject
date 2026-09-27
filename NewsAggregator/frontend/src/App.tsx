import { useEffect, useMemo, useState } from 'react';
import { Article, Genre } from './types';
import { formatDate } from './utils';
import './styles.css';

const genres: Genre[] = ['Finance', 'Sports', 'Politics', 'Science'];

const initialSession = {
  selectedGenre: 'Finance' as Genre,
  searchQuery: '',
  lastRefresh: ''
};

const loadSession = () => {
  try {
    const raw = localStorage.getItem('news-aggregator-session');
    return raw ? JSON.parse(raw) : initialSession;
  } catch {
    return initialSession;
  }
};

const saveSession = (session: typeof initialSession) => {
  localStorage.setItem('news-aggregator-session', JSON.stringify(session));
};

const loadBookmarks = (): string[] => {
  try {
    const raw = localStorage.getItem('news-aggregator-bookmarks');
    return raw ? JSON.parse(raw) : [];
  } catch {
    return [];
  }
};

const saveBookmarks = (bookmarks: string[]) => {
  localStorage.setItem('news-aggregator-bookmarks', JSON.stringify(bookmarks));
};

function App() {
  const [articles, setArticles] = useState<Article[]>([]);
  const [selectedGenre, setSelectedGenre] = useState<Genre>(initialSession.selectedGenre);
  const [searchQuery, setSearchQuery] = useState('');
  const [bookmarks, setBookmarks] = useState<string[]>([]);
  const [lastRefresh, setLastRefresh] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    const session = loadSession();
    setSelectedGenre(session.selectedGenre);
    setSearchQuery(session.searchQuery);
    setLastRefresh(session.lastRefresh);
    setBookmarks(loadBookmarks());
    fetchArticles();
  }, []);

  useEffect(() => {
    saveSession({ selectedGenre, searchQuery, lastRefresh });
  }, [selectedGenre, searchQuery, lastRefresh]);

  useEffect(() => {
    saveBookmarks(bookmarks);
  }, [bookmarks]);

  const fetchArticles = async () => {
    setLoading(true);
    setError('');

    try {
      const response = await fetch('/api/news');
      if (!response.ok) {
        throw new Error('Failed to load articles');
      }
      const data = (await response.json()) as Article[];
      setArticles(data);
      const refreshed = new Date().toISOString();
      setLastRefresh(refreshed);
    } catch (err) {
      setError((err as Error).message);
    } finally {
      setLoading(false);
    }
  };

  const toggleBookmark = (id: string) => {
    setBookmarks((current) =>
      current.includes(id) ? current.filter((item) => item !== id) : [...current, id]
    );
  };

  const filteredArticles = useMemo(() => {
    return articles
      .filter((article) => article.genre === selectedGenre)
      .filter((article) => {
        const normalized = searchQuery.trim().toLowerCase();
        return (
          article.title.toLowerCase().includes(normalized) ||
          article.summary.toLowerCase().includes(normalized)
        );
      });
  }, [articles, selectedGenre, searchQuery]);

  return (
    <div className="app-shell">
      <header className="header">
        <div>
          <h1>News Aggregator</h1>
          <p>FastAPI backend + React frontend</p>
        </div>
        <button className="refresh-button" onClick={fetchArticles} disabled={loading}>
          {loading ? 'Refreshing...' : 'Refresh'}
        </button>
      </header>

      <section className="controls">
        <div className="genres">
          {genres.map((genre) => (
            <button
              key={genre}
              className={genre === selectedGenre ? 'genre-button active' : 'genre-button'}
              onClick={() => setSelectedGenre(genre)}
            >
              {genre}
            </button>
          ))}
        </div>

        <input
          className="search-input"
          type="search"
          value={searchQuery}
          onChange={(event) => setSearchQuery(event.target.value)}
          placeholder="Search articles..."
        />
      </section>

      <section className="meta-row">
        <div>{filteredArticles.length} article(s) in {selectedGenre}</div>
        <div>Last refresh: {lastRefresh ? formatDate(lastRefresh) : 'never'}</div>
      </section>

      {error && <div className="error-banner">{error}</div>}

      <section className="articles-grid">
        {filteredArticles.map((article) => (
          <article key={article.id} className="article-card">
            <div className="article-header">
              <span className="article-genre">{article.genre}</span>
              <button className="bookmark-button" onClick={() => toggleBookmark(article.id)}>
                {bookmarks.includes(article.id) ? '★' : '☆'}
              </button>
            </div>
            <h2>{article.title}</h2>
            <p>{article.summary}</p>
            <div className="article-footer">
              <span>{article.source}</span>
              <a href={article.url} target="_blank" rel="noreferrer">
                Read more
              </a>
            </div>
          </article>
        ))}
      </section>
    </div>
  );
}

export default App;
