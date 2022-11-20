import { prismaClientMock } from '../../lib/mockup';

import { mainService } from '../../../api/main/main.service';
import { createFakeArticles } from '../../lib/utils';
import { getMonthsBefore } from '../../../utils/date';

describe('Testing main service', () => {
  it('Load static files', async () => {
    const staticFilelist = ['picture', 'short_intro', 'me'];
    const staticFileUrls = mainService.getStaticFileUrls(staticFilelist);

    expect(staticFileUrls).toHaveLength(staticFilelist.length);
    expect(staticFileUrls.filter(url => !!url.match(/\/public/))).toHaveLength(
      staticFilelist.length,
    );
  });

  it('Load articles from the DB', async () => {
    const articles = createFakeArticles();
    const recentArticles = articles.filter(
      article => article.updatedAt > getMonthsBefore(1),
    );
    prismaClientMock.article.findMany.mockResolvedValue(recentArticles);

    await expect(mainService.getRecentArticles(1)).resolves.toEqual(
      recentArticles,
    );
  });
});
