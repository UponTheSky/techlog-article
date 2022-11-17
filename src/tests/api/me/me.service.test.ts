import { MeServiceProvider } from '../../../api/me/me.service';
import { staticFileList } from '../../../api/me/me.dto';

describe('Testing me service', () => {
  const meServiceProvider = new MeServiceProvider();

  it('Load static files', async () => {
    const staticFiles = meServiceProvider.getStaticFiles(staticFileList);

    Object.values<string>(staticFiles).forEach(info => {
      expect(typeof info === 'string').toBeTruthy();
      expect(info.length > 0).toBeTruthy();
    });
  });
});
