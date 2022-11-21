import { RequestHandler, Router } from 'express';

import { Controller } from '../../common/interfaces/controller';

export class MainController implements Controller<ArticleDTO> {
  path: string;
  router: Router;
  serviceProvider = new MainServiceProvider();

  constructor() {
    this.path = '/api/main';
    this.router = Router();
    this.initRouter();
  }

  exportRouter(): Router {
    const exportedRouter = Router();
    exportedRouter.use(this.path, this.router);
    return exportedRouter;
  }

  initRouter(): void {
    this.router.get('/', this.getMainPage);
  }

  private getMainPage: RequestHandler = async (_request, response, next) => {
    try {
      const staticFileUrls = this.serviceProvider.getStaticFileUrls([
        'picture',
        'shortIntro',
      ]);
      const articles = await this.serviceProvider.getRecentArticles(1);

      response.json({
        staticFileUrls,
        articles,
        mainUrls: {
          me: '/api/me',
          articles: '/api/articles',
        },
      });
    } catch (error) {
      next(error);
    }
  };
}
