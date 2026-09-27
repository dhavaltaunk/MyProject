export type Genre = 'Finance' | 'Sports' | 'Politics' | 'Science';

export interface Article {
  id: string;
  title: string;
  genre: Genre;
  summary: string;
  source: string;
  date: string;
  url: string;
}
