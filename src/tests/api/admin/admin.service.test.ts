import { prismaClientMock } from '../../lib/mockup';

import { AdminLoginServiceProvider } from '../../../api/admin/admin.login.service';

import { createFakeArticles } from '../../lib/utils';
import { ADMIN_ARTICLES_NUMBER } from '../../../utils/config';

describe('Testing admin service', () => {
  const adminLoginServiceProvider = new AdminLoginServiceProvider();
  const userId = 'test';
  const password = 'test';
  const fakeUserId = 'fake';
  const fakePassword = 'fake';

  const articleInput = {
    thumbnail: '',
    title: 'test',
    excerpt: '',
    content: '',
    articleId: '1',
  };

  const articleSample = {
    ...articleInput,
    createdAt: new Date(Date.now()),
    updatedAt: new Date(Date.now()),
    id: 1,
  };

  describe('login and logout', () => {
    it('id and password validation', async () => {
      const token = await adminLoginServiceProvider.validateUserInfo({
        info: {
          userId,
          password,
        },
      });

      expect(token).toBeTruthy();

      expect(async () => {
        await adminLoginServiceProvider.validateUserInfo({
          info: {
            userId: fakeUserId,
            password: fakePassword,
          },
        });
      }).toThrow();
    });

    /* /admin/logout: TBA */
    // it('token revocation(or expiration)', async () => {

    // });
  });

  describe('admin articles CRUD', () => {
    it('CREATE', async () => {
      prismaClientMock.article.create.mockResolvedValue(articleSample);
      const createdArticle = await adminServiceProvider.create(articleInput);

      expect(createdArticle.articleId).toBe(articleInput.articleId);
    });

    it('READ a single article', async () => {
      prismaClientMock.article.findUnique.mockResolvedValue(articleSample);
      const readArticle = await adminServiceProvider.getUniqueArticle(
        articleSample.id,
      );

      expect(readArticle).toEqual(articleSample);

      prismaClientMock.article.findUnique.mockRejectedValue(new Error());

      expect(async () => {
        await adminServiceProvider.getUniqueArticle('fakeArticleId');
      }).toThrow();
    });

    it('READ with paging', async () => {
      const articles = createFakeArticles();
      const currentPage = 0;
      prismaClientMock.article.findMany.mockResolvedValue(articles);

      const articlesWithCurrentPage =
        await adminServiceProvider.getCurrentPageArticlesInfo(currentPage);

      expect(articlesWithCurrentPage).toHaveProperty('info');

      expect(articlesWithCurrentPage.info).toHaveProperty('totalArticlesCount');
      expect(articlesWithCurrentPage.info.totalArticlesCount).toBe(
        articles.length,
      );

      expect(articlesWithCurrentPage.info).toHaveProperty('totalPagesCount');
      expect(articlesWithCurrentPage.info.totalPagesCount).toBe(
        Math.ceil(articles.length / ADMIN_ARTICLES_NUMBER),
      );

      expect(articlesWithCurrentPage.info).toHaveProperty('currentPage');
      expect(articlesWithCurrentPage.info.currentPage).toBe(currentPage);

      expect(articlesWithCurrentPage).toHaveProperty('articles');
      expect(articles).toContain(articlesWithCurrentPage.articles);

      expect(async () => {
        await adminServiceProvider.getCurrentPageArticlesInfo(1000);
      }).toThrow();
    });

    it('UPDATE', async () => {
      const modifiedArticle = { ...articleSample, title: 'modified ' };
      prismaClientMock.article.update.mockResolvedValue(modifiedArticle);

      const updatedArticle = await adminServiceProvider.update(
        articleSample.articleId,
        { title: 'modified' },
      );

      expect(updatedArticle).toEqual(modifiedArticle);

      prismaClientMock.article.update.mockRejectedValue(new Error());
      expect(async () => {
        await adminServiceProvider.update('fakeArticleId', {});
      }).toThrow();
    });

    it('DELETE', async () => {
      prismaClientMock.article.delete.mockResolvedValue(articleSample);

      const deletedArticle = await adminServiceProvider.delete(
        articleSample.articleId,
      );

      expect(deletedArticle).toEqual(articleSample);

      prismaClientMock.article.delete.mockRejectedValue(new Error());
      expect(async () => {
        await adminServiceProvider.delete('fakeArticleId');
      }).toThrow();
    });
  });
});
