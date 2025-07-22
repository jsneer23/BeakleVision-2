import { SearchIndex, UtilsService } from '@/client';
import { SearchDataProvider } from '@/lib/search/api';

export class ProdAPIProvider implements SearchDataProvider {
  async provide(): Promise<SearchIndex> {
    const searchIndex = await UtilsService.searchIndex();

    if (searchIndex === undefined) {
      return Promise.reject(new Error('Failed to fetch search index'));
    }

    return searchIndex
  }
}