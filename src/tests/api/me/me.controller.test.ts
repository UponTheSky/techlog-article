import supertest from 'supertest';

import { app } from '../../../app';

const apiClient = supertest(app);

describe('Testing me controller', () => {
  it('GET /', async () => {
    const response = await apiClient
      .get('/api/me')
      .expect(200)
      .expect('Content-Type', /application\/json/);

    expect(response.body).toHaveProperty('meUrls');
    expect(response.body.meUrls).toHaveProperty('profile');
    expect(response.body.meUrls).toHaveProperty('shortIntro');
    expect(response.body.meUrls).toHaveProperty('education');
    expect(response.body.meUrls).toHaveProperty('workExperience');
    expect(response.body.meUrls).toHaveProperty('compSci');
    expect(response.body.meUrls).toHaveProperty('hobbies');
  });
});
