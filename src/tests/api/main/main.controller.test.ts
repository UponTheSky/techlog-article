import supertest from 'supertest';

import { app } from '../../../app';
import { prismaClient } from '../../../lib/db';

import { createFakeArticles } from '../../lib/utils';

const apiClient = supertest(app);

beforeAll(async () => {
  await prismaClient.$connect();
  console.log('DB connection open');

  await prismaClient.article.createMany({
    data: createFakeArticles(),
  });

  console.log('Fake articles successfully created');
});

describe('Testing main controller', () => {
  it('GET /', async () => {
    const response = await apiClient
      .get('/api/main')
      .expect(200)
      .expect('Content-Type', /application\/json/);

    expect(response.body).toHaveProperty('picture');
    expect(response.body).toHaveProperty('short_intro');
    expect(response.body).toHaveProperty('me');
    expect(response.body).toHaveProperty('articles');

    expect(response.body.articles[0]).toHaveProperty('thumbnail');
    expect(response.body.articles[0]).toHaveProperty('title');
    expect(response.body.articles[0]).toHaveProperty('excerpt');
    expect(response.body.articles[0]).toHaveProperty('articleId');
  });
});

afterAll(async () => {
  const deleteArticle = await prismaClient.article.deleteMany();
  console.log('all articles are cleaned');

  await prismaClient.$disconnect();
  console.log('DB connection closed');
});
