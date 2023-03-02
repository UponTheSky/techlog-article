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

    expect(response.body).toHaveProperty('meInfos');
    expect(Object.keys(response.body.meInfos)).toHaveLength(
      staticFileList.length,
    );

    staticFileList.forEach(file => {
      expect(response.body.meInfos).toHaveProperty(file);
    });
  });
});
