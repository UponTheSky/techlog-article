import bcrypt from 'bcrypt';
import { prismaClientMock } from '../../lib/mockup';

import { AdminLoginServiceProvider } from '../../../api/admin/admin.login.service';

import { createFakeArticles } from '../../lib/utils';
import { ADMIN_ARTICLES_NUMBER } from '../../../utils/config';
import { ArticlesServiceProvider } from '../../../api/articles/articles.service';
import { Prisma } from '@prisma/client';

describe('Testing admin service', () => {
  const adminLoginServiceProvider = new AdminLoginServiceProvider();
  const articlesServiceProvider = new ArticlesServiceProvider();
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
      prismaClientMock.adminUser.findUnique.mockResolvedValue({
        id: 0,
        email: 'test@test.com',
        firstName: 'root',
        lastName: 'test',
        passwordHash: await bcrypt.hash(password, 10),
        userId,
      });

      const token = await adminLoginServiceProvider.validateUserInfo({
        userId,
        password,
      });

      expect(token).toBeTruthy();
    });

    it('wrong id or password', async () => {
      prismaClientMock.adminUser.findUnique.mockResolvedValue(null);

      expect(async () => {
        await adminLoginServiceProvider.validateUserInfo({
          userId,
          password: fakePassword,
        });
      }).rejects.toThrow('either user id or password is invalid');

      expect(async () => {
        await adminLoginServiceProvider.validateUserInfo({
          userId: fakeUserId,
          password,
        });
      }).rejects.toThrow('either user id or password is invalid');
    });

    /* /admin/logout: TBA */
    // it('token revocation(or expiration)', async () => {

    // });
  });

  describe('admin articles CRUD', () => {
    it('CREATE', async () => {
      prismaClientMock.article.create.mockResolvedValue(articleSample);
      const createdArticle = await articlesServiceProvider.create(articleInput);

      expect(createdArticle.articleId).toBe(articleInput.articleId);
    });

    it('READ a single article', async () => {
      prismaClientMock.article.findUnique.mockResolvedValue(articleSample);
      const readArticle = await articlesServiceProvider.getUniqueArticle(
        articleSample.articleId,
      );

      expect(readArticle).toEqual(articleSample);

      prismaClientMock.article.findUnique.mockResolvedValue(null);

      expect(async () => {
        await articlesServiceProvider.getUniqueArticle('fakeArticleId');
      }).rejects.toThrow();
    });

    it('READ with paging', async () => {
      const articles = createFakeArticles();
      const currentPage = 0;
      prismaClientMock.article.findMany.mockResolvedValue(articles);
      prismaClientMock.article.count.mockResolvedValue(articles.length);

      const articlesWithCurrentPage =
        await articlesServiceProvider.getCurrentPageArticlesInfo(
          currentPage,
          ADMIN_ARTICLES_NUMBER,
        );

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

      prismaClientMock.article.findMany.mockResolvedValue([]);
      expect(async () => {
        await articlesServiceProvider.getCurrentPageArticlesInfo(
          1000,
          ADMIN_ARTICLES_NUMBER,
        );
      }).rejects.toThrow();
    });

    it('UPDATE', async () => {
      const modifiedArticle = { ...articleSample, title: 'modified ' };
      prismaClientMock.article.update.mockResolvedValue(modifiedArticle);

      const updatedArticle = await articlesServiceProvider.update(
        articleSample.articleId,
        { title: 'modified' },
      );

      expect(updatedArticle).toEqual(modifiedArticle);

      prismaClientMock.article.update.mockRejectedValue(
        new Prisma.NotFoundError(''),
      );
      expect(async () => {
        await articlesServiceProvider.update('fakeArticleId', {});
      }).rejects.toThrow();
    });

    it('DELETE', async () => {
      prismaClientMock.article.delete.mockResolvedValue(articleSample);

      const deletedArticle = await articlesServiceProvider.delete(
        articleSample.articleId,
      );

      expect(deletedArticle).toEqual(articleSample);

      prismaClientMock.article.delete.mockRejectedValue(
        new Prisma.NotFoundError(''),
      );
      expect(async () => {
        await articlesServiceProvider.delete('fakeArticleId');
      }).rejects.toThrow();
    });
  });
});
