import { ServiceProvider } from '../../common/interfaces/service';
import {
  ArticleDTO,
  CurrentPageArticlesResponse,
  IndividualArticlesResponse,
} from './articles.dto';
import { ArticlesRepository } from './articles.repository';
import { ARTICLES_ARTICLES_NUMBER } from '../../utils/config';
import { NotFoundError } from '../../common/exceptions';

export class ArticlesServiceProvider implements ServiceProvider<ArticleDTO> {
  repository = new ArticlesRepository();

  getCurrentPageArticlesInfo = async (
    currentPage: number,
  ): Promise<CurrentPageArticlesResponse> => {
    const { totalArticlesCount, totalPagesCount } =
      await this.getArticlesInfo();
    const skip = currentPage * ARTICLES_ARTICLES_NUMBER;
    const take = ARTICLES_ARTICLES_NUMBER;

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

  private getArticlesInfo = async (): Promise<{
    [key: symbol | string]: number;
  }> => {
    const totalArticlesCount = await this.repository.count();
    const totalPagesCount = Math.ceil(
      totalArticlesCount / ARTICLES_ARTICLES_NUMBER,
    );

    return { totalArticlesCount, totalPagesCount };
  };
}
