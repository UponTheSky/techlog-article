import supertest from 'supertest';

import { app } from '../../../app';
import { prismaClient } from '../../../lib/db';

import { createFakeArticles } from '../../lib/utils';
import {
  ARTICLES_ARTICLES_NUMBER,
  ARTICLES_DEFAULT_CURRENT_PAGE,
} from '../../../utils/config';

const apiClient = supertest(app);
const fakeArticles = createFakeArticles();

beforeAll(async () => {
  await prismaClient.$connect();
  console.log('DB connection open');

  await prismaClient.article.createMany({
    data: fakeArticles,
  });

  console.log('Fake articles successfully created');
});

describe('Testing articles controller', () => {
  const currentPage = ARTICLES_DEFAULT_CURRENT_PAGE;

  it('GET / default currentPage is ARTICLES_DEFAULT_CURRENT_PAGE', async () => {
    const response = await apiClient.get('/api/articles').expect(200);

    expect(response.body).toHaveProperty('info');
    expect(response.body.info).toHaveProperty('currentPage');
    expect(response.body.info.currentPage).toBe(currentPage);
  });

  it(`GET /?currentPage=${currentPage}`, async () => {
    const response = await apiClient
      .get(`/api/articles/?currentPage=${currentPage}`)
      .expect(200)
      .expect('Content-Type', /application\/json/);

    expect(response.body.info).toHaveProperty('totalArticlesCount');
    expect(response.body.info).toHaveProperty('totalPagesCount');
    expect(response.body.info.currentPage).toBe(currentPage);

    expect(response.body).toHaveProperty('articles');
    expect(response.body.articles).toHaveLength(ARTICLES_ARTICLES_NUMBER);

    for (let i = 0; i < response.body.articles.length - 1; i++) {
      expect(
        response.body.articles[i].updatedAt >=
          response.body.articles[i + 1].updatedAt,
      ).toBeTruthy();
    }
  });

  it('GET /?currentPage when currentPage >= (totalPagesCount / articlesPerPage)', async () => {
    const response = await apiClient.get(
      `/api/articles/?currentPage=${currentPage}`,
    );

    const {
      info: { totalPagesCount },
    } = response.body;
    await apiClient
      .get(`/api/articles/?currentPage=${totalPagesCount}`)
      .expect(404);
  });

  it('GET /:articleId', async () => {
    const response = await apiClient.get('/api/articles/2').expect(200);

    const secondArticle = fakeArticles[1];
    expect(response.body.articleId).toEqual(secondArticle.articleId);
  });

  it('GET /:articleId when articleId does not exist', async () => {
    await apiClient.get('/api/articles/noneExists').expect(404);
  });
});

afterAll(async () => {
  const deleteArticle = await prismaClient.article.deleteMany();
  deleteArticle.count > 0
    ? console.log('all articles are cleaned')
    : console.error('database error while testing');

  await prismaClient.$disconnect();
  console.log('DB connection closed');
});
