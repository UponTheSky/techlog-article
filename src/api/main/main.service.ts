import { ServiceProvider } from '../../common/interfaces/service';
import { MainResponse, ArticleDTO, StaticFileList } from './main.dto';
import { getMonthsBefore } from '../../utils/date';
import { STATIC_ROOT } from '../../utils/config';
import { MainRepository } from './main.repository';

export class MainServiceProvider implements ServiceProvider<ArticleDTO> {
  repository = new MainRepository();

  getStaticFileUrls = (
    staticFileList: StaticFileList,
  ): MainResponse['staticFileUrls'] => {
    let staticFileUrls = {} as MainResponse['staticFileUrls'];
    staticFileList.forEach(file => {
      let ext = '';
      switch (file) {
        case 'picture':
          ext = 'png';
          break;
        case 'shortIntro':
          ext = 'txt';
          break;
        default:
          break;
      }
      staticFileUrls = {
        ...staticFileUrls,
        [file]: `/${STATIC_ROOT}/${file}.${ext}`,
      };
    });

    return staticFileUrls;
  };

  getRecentArticles = async (months: number) => {
    const monthsBefore = getMonthsBefore(months);
    const recentArticles = await this.repository.findMany(monthsBefore);

    return recentArticles;
  };
}
