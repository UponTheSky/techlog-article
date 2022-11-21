import { RequestHandler, Router } from 'express';

import { Controller } from '../../common/interfaces/controller';
import { staticFileList } from './me.dto';
import { MeServiceProvider } from './me.service';

// eslint-disable-next-line @typescript-eslint/no-explicit-any
export class MeController implements Controller<any> {
  path: string;
  router: Router;
  serviceProvider = new MeServiceProvider();

  constructor() {
    this.path = '/api/me';
    this.router = Router();
    this.initRouter();
  }

  exportRouter(): Router {
    const exportedRouter = Router();
    exportedRouter.use(this.path, this.router);
    return exportedRouter;
  }

  initRouter(): void {
    this.router.get('/', this.getMePage);
  }

  private getMePage: RequestHandler = (_request, response, next) => {
    try {
      const meUrls = this.serviceProvider.getStaticFileUrls(staticFileList);
      response.json({
        meUrls,
      });
    } catch (error) {
      next(error);
    }
  };
}
