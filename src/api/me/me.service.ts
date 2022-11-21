import { MeResponse, StaticFileList } from './me.dto';
import { STATIC_ROOT } from '../../utils/config';
import { ServiceProvider } from '../../common/interfaces/service';

// eslint-disable-next-line @typescript-eslint/no-explicit-any
export class MeServiceProvider implements ServiceProvider<any> {
  repository = undefined;

  getStaticFileUrls = (
    staticFileList: StaticFileList,
  ): MeResponse['meUrls'] => {
    let staticFileUrls = {} as MeResponse['meUrls'];
    const rootPath = `${STATIC_ROOT}/me`;

    staticFileList.forEach(file => {
      const ext = file === 'profile' ? 'png' : 'md';
      staticFileUrls = {
        ...staticFileUrls,
        [file]: `/${rootPath}/${file}.${ext}`,
      };
    });

    return staticFileUrls;
  };
}
