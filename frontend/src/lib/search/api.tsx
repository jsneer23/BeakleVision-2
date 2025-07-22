import { SearchIndex } from '@/client';

export interface SearchDataProvider {
  provide(): Promise<SearchIndex>;
}

export interface SearchDataFilterer {
  filter(data: SearchIndex, query: string): SearchIndex;
}