import { MeServiceProvider } from '../../../api/me/me.service';
import { staticFileList } from '../../../api/me/me.dto';

describe('Testing me service', () => {
  const meServiceProvider = new MeServiceProvider();

  it('Load static files', async () => {
    const meResponse = {
      meUrl: {
        profile: '/public/me/profile.png',
        shortIntro: '/public/me/shortIntro.md',
        workExperience: '/public/me/workExperience.md',
        education: '/public/me/education.md',
        compSci: '/public/me/compSci.md',
        hobbies: '/public/me/hobbies.md',
        externalLinks: '/public/me/externalLinks.md',
      },
    };
    const staticFileUrls = meServiceProvider.getStaticFileUrls(staticFileList);

    expect(
      Object.values<string>(staticFileUrls).filter(
        url => !!url.match(/\/public\/me\/\w+\.(png|md)/),
      ),
    ).toHaveLength(staticFileList.length);

    expect(staticFileUrls).toEqual(meResponse['meUrl']);
  });
});
