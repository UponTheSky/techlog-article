import supertest from 'supertest';
import bcrypt from 'bcrypt';

import { app } from '../../../app';
import { prismaClient } from '../../../lib/db';

import { createFakeArticles } from '../../lib/utils';
import { ADMIN_ARTICLES_NUMBER } from '../../../utils/config';

const apiClient = supertest(app);
const fakeArticles = createFakeArticles();
const currentPage = 0;
let token: string;
const fakeToken = 'fakeToken';

beforeAll(async () => {
  // MySQL DB
  await prismaClient.$connect();
  console.log('MySQL DB connection open');

  await prismaClient.article.createMany({
    data: fakeArticles,
  });

  console.log('Fake articles successfully created');

  const passwordHash = await bcrypt.hash('test', 10);
  await prismaClient.adminUser.create({
    data: {
      userId: 'test',
      email: 'test@test.com',
      firstName: 'root',
      lastName: 'test',
      passwordHash,
    },
  });

  const loginResponse = await apiClient.post('/admin/login').send({
    userId: 'test',
    password: 'test',
  });
  token = loginResponse.body.token;

  console.log('a jwt token has been successfully generated');

  // Redis Cache DB
  // TBA
});

describe('Testing admin page & login', () => {
  describe('case #0: redirect', () => {
    it('GET /api/admin => redirect to /api/admin/articles', async () => {
      await apiClient
        .get('api/admin')
        .expect(301)
        .expect('Location', '/api/admin/articles');
    });
  });

  describe('case #1: without a token', () => {
    it('GET /api/admin/articles', async () => {
      await apiClient.get('/api/admin/articles').expect(401);

      await apiClient
        .get(`/api/admin/articles?currentPage=${currentPage}`)
        .expect(401);
    });

    it('POST /api/admin/login: valid case', async () => {
      const response = await apiClient
        .post('/api/admin/login')
        .send({
          userId: 'test',
          password: 'test',
        })
        .expect(301)
        .expect('Location', '/api/admin/articles');

      expect(response.body).toHaveProperty('token');
    });

    it('POST /api/admin/login: invalid case', async () => {
      await apiClient
        .post('/api/admin/login')
        .send({
          userId: 'fakeUserId',
          password: 'test',
        })
        .expect(401);

      await apiClient
        .post('/api/admin/login')
        .send({
          userId: 'test',
          password: 'fakeUserPassword',
        })
        .expect(401);
    });
  });

  describe('case #2: valid token', () => {
    const totalPagesCount = Math.ceil(
      fakeArticles.length / ADMIN_ARTICLES_NUMBER,
    );
    it(`GET /api/admin/articles`, async () => {
      const response = await apiClient
        .get('/api/admin/articles')
        .auth(token, { type: 'bearer' })
        .expect(200);

      expect(response.body).toHaveProperty('info');
      expect(response.body.info).toHaveProperty('currentPage');
      expect(response.body.info.currentPage).toBe(currentPage);
    });

    it(`GET /api/admin/articles?currentPage=${currentPage}`, async () => {
      const response = await apiClient
        .get(`/api/admin/articles?=${currentPage}`)
        .auth(token, { type: 'bearer' })
        .expect(200)
        .expect('Content-Type', /application\/json/);

      expect(response.body.info).toHaveProperty('totalArticlesCount');
      expect(response.body.info).toHaveProperty('totalPagesCount');
      expect(response.body.info.currentPage).toBe(currentPage);

      expect(response.body).toHaveProperty('articles');
      expect(response.body.articles).toHaveLength(ADMIN_ARTICLES_NUMBER);

      for (let i = 0; i < response.body.articles.length - 1; i++) {
        expect(
          response.body.articles[i].updatedAt >=
            response.body.articles[i + 1].updatedAt,
        ).toBeTruthy();
      }
    });

    it(`GET ?currentPage when currentPage >= (totalPagesCount / articlesPerPage)`, async () => {
      await apiClient
        .get(`/api/admin/articles?${totalPagesCount}`)
        .auth(token, { type: 'bearer' })
        .expect(404);
    });

    it('GET /api/admin/login', async () => {
      await apiClient
        .get('/api/admin/login')
        .auth(token, { type: 'bearer' })
        .expect(301)
        .expect('Location', '/api/admin/articles');
    });

    it('POST /api/admin/login', async () => {
      await apiClient
        .post('/api/admin/login')
        .auth(token, { type: 'bearer' })
        .send({
          userId: 'test',
          password: 'test',
        })
        .expect(301)
        .expect('Location', '/api/admin/articles');
    });
  });

  describe('case #3: invalid(either wrong or expired token', () => {
    it('GET /api/admin/articles', async () => {
      await apiClient
        .get('/api/admin/articles')
        .auth(fakeToken, { type: 'bearer' })
        .expect(401);

      await apiClient
        .get(`/api/admin/articles?currentPage=${currentPage}`)
        .auth(fakeToken, { type: 'bearer' })
        .expect(401);
    });

    it('POST /api/admin/login', async () => {
      await apiClient
        .post('/api/admin/login')
        .auth(fakeToken, { type: 'bearer' })
        .send({
          userId: 'test',
          password: 'test',
        })
        .expect(301)
        .expect('Location', '/api/admin/articles');
    });
  });

  /* /admin/logout: TBA(using token blocking mechanism using Redis cache) */

  // describe('logout: revoking the current token(if there is)', () => {
  //   const oldToken = token;
  //   it('GET /admin/logout', async () => {
  //     await apiClient
  //       .get('/admin/logout')
  //       .auth(oldToken, {'type': 'bearer'})
  //       .expect(204);

  //     await apiClient
  //       .get('/admin')
  //       .auth(oldToken, {'type': 'bearer'})
  //       .expect(401);
  //   });
  // });
});

describe('admin article CRUD /api/admin/articles', () => {
  const testArticleId = '1';
  const fakeArticleId = 'fake';
  const testArticle = {
    thumbnail: '',
    title: 'test',
    excerpt: 'test',
    content: 'test',
    articleId: 'test',
  };

  const testArticleWithoutId = {
    thumbnail: '',
    title: 'test',
    excerpt: 'test',
    content: 'test',
  };

  const testArticleWithoutTitle = {
    thumbnail: '',
    excerpt: 'test',
    content: 'test',
    articleId: 'test',
  };

  describe('CREATE', () => {
    it('fake or no token', async () => {
      await apiClient
        .post('/api/admin/articles')
        .auth(fakeToken, { type: 'bearer' })
        .send(testArticle)
        .expect(401);

      await apiClient.post('/api/admin/articles').send(testArticle).expect(401);
    });

    describe('valid token', () => {
      it('when bad objects are passed over', async () => {
        const withoutIdResponse = await apiClient
          .post('/api/admin/articles')
          .auth(token, { type: 'bearer' })
          .send(testArticleWithoutId)
          .expect(400);

        expect(withoutIdResponse.body.error).toContain('id');

        const withoutTitleResponse = await apiClient
          .post('/api/admin/articles')
          .auth(token, { type: 'bearer' })
          .send(testArticleWithoutTitle)
          .expect(400);

        expect(withoutTitleResponse.body.error).toContain('title');
      });

      it('when a normal object is passed over', async () => {
        await apiClient
          .post('/api/admin/articles')
          .auth(token, { type: 'bearer' })
          .send(testArticle)
          .expect(201)
          .expect('Content-Type', /application\/json/);
      });
    });
  });

  describe('READ', () => {
    it('fake or no token', async () => {
      await apiClient
        .get(`/api/admin/articles/${testArticleId}`)
        .auth(fakeToken, { type: 'bearer' })
        .expect(401);

      await apiClient.get('/admin/articles').expect(401);
    });

    it('valid token', async () => {
      await apiClient
        .get(`/api/admin/articles/${testArticleId}`)
        .auth(token, { type: 'bearer' })
        .expect(200);

      await apiClient
        .get(`/api/admin/articles/${fakeArticleId}`)
        .auth(token, { type: 'bearer' })
        .expect(404);
    });
  });

  describe('UPDATE', () => {
    it('fake or no token', async () => {
      await apiClient
        .put(`/api/admin/articles/${testArticleId}`)
        .auth(fakeToken, { type: 'bearer' })
        .expect(401);

      await apiClient.put(`/admin/articles/${testArticleId}`).expect(401);
    });

    it('valid or no token', async () => {
      await apiClient
        .put(`/api/admin/articles/${testArticleId}`)
        .auth(token, { type: 'bearer' })
        .send({ title: '' })
        .expect(200);

      await apiClient
        .put(`/api/admin/articles/${fakeArticleId}`)
        .auth(token, { type: 'bearer' })
        .send({ title: '' })
        .expect(404);
    });
  });

  describe('DELETE', () => {
    it('fake or no token', async () => {
      await apiClient
        .delete(`/api/admin/articles/${testArticleId}`)
        .auth(fakeToken, { type: 'bearer' })
        .expect(401);

      await apiClient
        .delete(`/api/admin/articles/${testArticleId}`)
        .expect(401);
    });

    it('valid token', async () => {
      await apiClient
        .delete(`/api/admin/articles/${testArticleId}`)
        .auth(token, { type: 'bearer' })
        .expect(204);

      await apiClient
        .delete(`/api/admin/articles/${fakeArticleId}`)
        .auth(token, { type: 'bearer' })
        .expect(404);
    });
  });
});

afterAll(async () => {
  const deleteArticle = await prismaClient.article.deleteMany();
  deleteArticle.count === 0
    ? console.log('all articles are cleaned')
    : console.error('database error while testing');

  const deleteAdminUser = await prismaClient.adminUser.deleteMany();
  deleteAdminUser.count === 0
    ? console.log('all admin users are cleaned')
    : console.error('database error while testing');

  await prismaClient.$disconnect();
  console.log('DB connection closed');
});
