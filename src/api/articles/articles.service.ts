import { ServiceProvider } from '../../common/interfaces/service';
import {
  ArticleDTO,
  CurrentPageArticlesResponse,
  IndividualArticlesResponse,
} from './articles.dto';
import { ArticlesRepository } from './articles.repository';
import { NotFoundError } from '../../common/exceptions';

export class ArticlesServiceProvider implements ServiceProvider<ArticleDTO> {
  repository = new ArticlesRepository();

  // READ
  getCurrentPageArticlesInfo = async (
    currentPage: number,
    articlesPerPage: number,
  ): Promise<CurrentPageArticlesResponse> => {
    const { totalArticlesCount, totalPagesCount } = await this.getArticlesInfo(
      articlesPerPage,
    );
    const skip = currentPage * articlesPerPage;
    const take = articlesPerPage;

    const currentPageArticles = await this.repository.findMany({ skip, take });
    if (!currentPageArticles || currentPageArticles.length === 0) {
      throw new NotFoundError(`articles on ${currentPage} have not been found`);
    }

    return {
      info: {
        totalArticlesCount,
        totalPagesCount,
        currentPage,
      },
      articles: currentPageArticles,
    };
  };

  getUniqueArticle = async (
    articleId: ArticleDTO['articleId'],
  ): Promise<IndividualArticlesResponse> => {
    const article = await this.repository.findUnique(articleId);

    if (!article) {
      throw new NotFoundError(
        `articles with articleId ${articleId} has not been found`,
      );
    }
    return article;
  };

  private getArticlesInfo = async (
    articlesPerPage: number,
  ): Promise<{
    [key: symbol | string]: number;
  }> => {
    const totalArticlesCount = await this.repository.count();
    const totalPagesCount = Math.ceil(totalArticlesCount / articlesPerPage);

    return { totalArticlesCount, totalPagesCount };
  };

  // CREATE
  create = async (data: Partial<ArticleDTO>): Promise<ArticleDTO> => {
    return await this.repository.create(data);
  };

  // UPDATE
  update = async (
    articleId: ArticleDTO['articleId'],
    data: Partial<ArticleDTO>,
  ): Promise<ArticleDTO> => {
    const updatedArticle = await this.repository.updateById(articleId, data);

    if (!updatedArticle) {
      throw new NotFoundError(
        `an article with id ${articleId} has not been found`,
      );
    }

    return updatedArticle;
  };

  // DELETE
  delete = async (articleId: ArticleDTO['articleId']) => {
    const deletedArticle = await this.repository.deleteById(articleId);

    if (!deletedArticle) {
      throw new NotFoundError(
        `an article with id ${articleId} has not been found`,
      );
    }

    return deletedArticle;
  };
}
