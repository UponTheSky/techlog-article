import { prismaClientMock } from '../../lib/mockup';

import { AdminServiceProvider } from '../../../api/admin/admin.service';

describe('Testing admin service', () => {
  const adminServiceProvider = new AdminServiceProvider();
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
      const token = await adminServiceProvider.validateUserInfo({
        info: {
          userId,
          password,
        },
      });

      expect(token).toBeTruthy();

      expect(async () => {
        await adminServiceProvider.validateUserInfo({
          info: {
            fakeUserId,
            fakePassword,
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

    it('READ', async () => {
      prismaClientMock.article.findUnique.mockResolvedValue(articleSample);
      const readArticle = await adminServiceProvider.read(articleSample.id);

      expect(readArticle).toEqual(articleSample);

      expect(async () => {
        await adminServiceProvider.read('fakeArticleId');
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

      expect(async () => {
        await adminServiceProvider.delete('fakeArticleId');
      }).toThrow();
    });
  });
});
