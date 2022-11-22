import supertest from 'supertest';
import { staticFileList } from '../../../api/me/me.dto';

import { app } from '../../../app';

const apiClient = supertest(app);

describe('Testing me controller', () => {
  it('GET /', async () => {
    const response = await apiClient
      .get('/api/me')
      .expect(200)
      .expect('Content-Type', /application\/json/);

    expect(response.body).toHaveProperty('meUrls');
    expect(Object.keys(response.body.meUrls)).toHaveLength(
      staticFileList.length,
    );

    staticFileList.forEach(file => {
      expect(response.body.meUrls).toHaveProperty(file);
    });
  });
});
