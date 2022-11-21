import { prismaClientMock } from '../../lib/mockup';

import { MainServiceProvider } from '../../../api/main/main.service';
import { createFakeArticles } from '../../lib/utils';
import { getMonthsBefore } from '../../../utils/date';

describe('Testing main service', () => {
  const mainServiceProvider = new MainServiceProvider();

  it('Load static files', async () => {
    const staticFileList = ['picture', 'shortIntro'] as (
      | 'picture'
      | 'shortIntro'
    )[];
    const staticFileUrls =
      mainServiceProvider.getStaticFileUrls(staticFileList);

    expect(
      Object.values<string>(staticFileUrls).filter(
        url => !!url.match(/\/public/),
      ),
    ).toHaveLength(staticFileList.length);
  });

  it('Load articles from the DB', async () => {
    const articles = createFakeArticles();
    const recentArticles = articles.filter(
      article => article.updatedAt > getMonthsBefore(1),
    );
    prismaClientMock.article.findMany.mockResolvedValue(recentArticles);

    await expect(mainServiceProvider.getRecentArticles(1)).resolves.toEqual(
      recentArticles,
    );
  });
});
