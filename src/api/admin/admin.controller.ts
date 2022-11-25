import { RequestHandler, Router } from 'express';

import { ArticleDTO, LoginDTO } from './admin.dto';
import { Controller } from '../../common/interfaces/controller';
import { ArticlesServiceProvider } from '../articles/articles.service';
import { AdminLoginServiceProvider } from './admin.login.service';
import {
  ADMIN_ARTICLES_NUMBER,
  ARTICLES_DEFAULT_CURRENT_PAGE,
} from '../../utils/config';
import { BadRequestError } from '../../common/exceptions';
import {
  jwtHandler,
  jwtAdminArticlesHandler,
} from '../../utils/middlewares/jwt.middleware';

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
    exportedRouter.use(jwtAdminArticlesHandler);
    exportedRouter.use(this.path, this.router);
    return exportedRouter;
  }

  initRouter(): void {
    // CRUD
    this.router.get('/articles', this.getCurrentPage);
    this.router.get('/articles/:articleId', this.getIndividualPage);
    this.router.post('/articles', this.createIndividualArticle);
    this.router.put('/articles/:articleId', this.updateIndividualArticle);
    this.router.delete('/articles/:articleId', this.deleteIndividualArticle);

    // login
    this.router.post('/login', this.login);

    // logout(TBA)
  }

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
  private createIndividualArticle: RequestHandler = async (
    request,
    response,
    next,
  ) => {
    try {
      const newArticle = await this.serviceProvider.create(
        request.body as Partial<ArticleDTO>,
      );

      response.status(201).json(newArticle);
    } catch (error) {
      next(error);
    }
  };

  // UPDATE
  private updateIndividualArticle: RequestHandler = async (
    request,
    response,
    next,
  ) => {
    try {
      const articleId = request.params.articleId;
      const data = request.body as Partial<ArticleDTO>;

      if (!articleId) {
        throw new BadRequestError(
          "need to specify the article's id for update",
        );
      }

      if (!data) {
        throw new BadRequestError('no data provided for updating the article');
      }

      const updatedPage = await this.serviceProvider.update(articleId, data);

      response.json(updatedPage);
    } catch (error) {
      next(error);
    }
  };

  // DELETE
  private deleteIndividualArticle: RequestHandler = async (
    request,
    response,
    next,
  ) => {
    try {
      const articleId = request.params.articleId;

      if (!articleId) {
        throw new BadRequestError(
          "need to specify the article's id for update",
        );
      }

      const deletedArticle = await this.serviceProvider.delete(articleId);

      response.status(204).json(deletedArticle);
    } catch (error) {
      next(error);
    }
  };

  // login
  private login: RequestHandler = async (request, response, next) => {
    try {
      const loginDTO = request.body as LoginDTO;

      const token = await this.loginServiceProvider.validateUserInfo(loginDTO);

      response
        .status(301)
        .json({ token })
        .redirect(`${request.baseUrl}/articles`);
    } catch (error) {
      next(error);
    }
  };
}
