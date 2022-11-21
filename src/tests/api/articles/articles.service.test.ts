import { prismaClientMock } from '../../lib/mockup';

import { ArticlesServiceProvider } from '../../../api/articles/articles.service';
import { createFakeArticles } from '../../lib/utils';
import {
  ARTICLES_ARTICLES_NUMBER,
  ARTICLES_DEFAULT_CURRENT_PAGE,
} from '../../../utils/config';

describe('Testing article service', () => {
  const articlesServiceProvider = new ArticlesServiceProvider();
  const currentPage = ARTICLES_DEFAULT_CURRENT_PAGE;
  const nextPage = currentPage + 1;
  const articlesPerPage = ARTICLES_ARTICLES_NUMBER;
  const totalArticles = createFakeArticles();

  it(`GET /?currentPage=${nextPage}`, async () => {
    const nextPageArticles = totalArticles
      .sort((a, b) => b.updatedAt.getTime() - a.updatedAt.getTime())
      .slice(articlesPerPage * nextPage);
    prismaClientMock.article.findMany.mockResolvedValue(nextPageArticles);
    const responseArticles = (
      await articlesServiceProvider.getCurrentPageArticlesInfo(nextPage)
    ).articles;

    expect(responseArticles[0]).toEqual(nextPageArticles[0]);
  });

  it('GET /:articleId => Load a single article from the DB', async () => {
    const articleId = '1';
    const article1 = totalArticles.find(
      article => article.articleId === articleId,
    );
    if (!article1) {
      return;
    }

    prismaClientMock.article.findUnique.mockResolvedValue(article1);
    await expect(
      articlesServiceProvider.getUniqueArticle(articleId),
    ).resolves.toEqual(article1);
  });
});
