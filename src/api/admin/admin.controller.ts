import { RequestHandler, Router } from 'express';

import { ArticleDTO } from './admin.dto';
import { Controller } from '../../common/interfaces/controller';
import { ArticlesServiceProvider } from '../articles/articles.service';
import { AdminLoginServiceProvider } from './admin.login.service';
import {
  ADMIN_ARTICLES_NUMBER,
  ARTICLES_DEFAULT_CURRENT_PAGE,
} from '../../utils/config';
import { BadRequestError } from '../../common/exceptions';
import { jwtHandler } from '../../utils/middlewares/jwt.middleware';

export class AdminController implements Controller<ArticleDTO> {
  path: string;
  router: Router;
  serviceProvider = new ArticlesServiceProvider();
  loginServiceProvider = new AdminLoginServiceProvider();

  constructor() {
    this.path = '/api/admin';
    this.router = Router();
    this.initRouter();
  }

  exportRouter(): Router {
    const exportedRouter = Router();
    exportedRouter.use(jwtHandler);
    exportedRouter.use(this.path, this.router);
    return exportedRouter;
  }

  initRouter(): void {
    this.router.get('/', this.defaultPageRouter);
    this.router.get('/articles', this.getCurrentPage);
    this.router.get('/articles/:articleId', this.getIndividualPage);
    // this.router.post('/articles', this.)
    // this.router.put('/articles/:articleId)
    // this.router.delete('/articles/:articleId)
    this.router.post('/login', this.login);
  }

  // default page router
  private defaultPageRouter: RequestHandler = async (
    request,
    response,
    next,
  ) => {
    try {
      response.status(301).redirect(`${request.baseUrl}/articles`);
      return;
    } catch (error) {
      next(error);
    }
  };

  // articles

  // READ
  private getCurrentPage: RequestHandler = async (request, response, next) => {
    try {
      const currentPageQuery = request.query.currentPage;

      if (currentPageQuery && typeof currentPageQuery !== 'string') {
        throw new BadRequestError(
          'input query is not valid: only one query value should be passed to',
        );
      }

      const currentPage =
        Number(request.query.currentPage as string) ||
        ARTICLES_DEFAULT_CURRENT_PAGE;
      const currentPageArticlesInfo =
        await this.serviceProvider.getCurrentPageArticlesInfo(
          currentPage,
          ADMIN_ARTICLES_NUMBER,
        );

      response.json(currentPageArticlesInfo);
    } catch (error) {
      next(error);
    }
  };

  private getIndividualPage: RequestHandler = async (
    request,
    response,
    next,
  ) => {
    try {
      const articleId = request.params.articleId;
      if (!articleId) {
        throw new BadRequestError('article Id has not been passed to');
      }

      const article = await this.serviceProvider.getUniqueArticle(articleId);

      response.json(article);
    } catch (error) {
      next(error);
    }
  };

  // CREATE

  // UPDATE

  // DELETE

  // login
  private login: RequestHandler = async (request, response, next) => {
    try {
      if (!request.decodedToken) {
        const { info } = request.body;

        const token = await this.loginServiceProvider.validateUserInfo(info);

        response.status(301).json({ token }).redirect(request.baseUrl);
      } else {
      }
    } catch (error) {
      next(error);
    }
  };
}
