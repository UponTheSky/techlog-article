import { RequestHandler, Router } from 'express';

import { ArticleDTO } from './articles.dto';
import { Controller } from '../../common/interfaces/controller';
import { ArticlesServiceProvider } from './articles.service';
import { ARTICLES_DEFAULT_CURRENT_PAGE } from '../../utils/config';
import { BadRequestError, NotFoundError } from '../../common/exceptions';

export class ArticlesController implements Controller<ArticleDTO> {
  path: string;
  router: Router;
  serviceProvider = new ArticlesServiceProvider();

  constructor() {
    this.path = '/api/articles';
    this.router = Router();
    this.initRouter();
  }

  exportRouter(): Router {
    const exportedRouter = Router();
    exportedRouter.use(this.path, this.router);
    return exportedRouter;
  }

  initRouter(): void {
    this.router.get('/', this.getCurrentPage);
    this.router.get('/:articleId', this.getIndividualPage);
  }

  private getCurrentPage: RequestHandler = async (request, response, next) => {
    try {
      const currentPageQuery = request.query.currentPage;

      if (!currentPageQuery || typeof currentPageQuery !== 'string') {
        throw new BadRequestError(
          'input query is not valid: only one query value should be passed to',
        );
      }

      const currentPage =
        Number(request.query.currentPage as string) ||
        ARTICLES_DEFAULT_CURRENT_PAGE;
      const currentPageArticlesInfo =
        await this.serviceProvider.getCurrentPageArticlesInfo(currentPage);

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

      if (!article) {
        throw new NotFoundError(`no corresponding data to ${articleId}`);
      }

      response.json(article);
    } catch (error) {
      next(error);
    }
  };
}
