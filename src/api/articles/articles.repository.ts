import { Repository } from '../../common/interfaces/repository';
import { ArticleDTO } from './articles.dto';
import { prismaClient } from '../../lib/db';
import { InternalError } from '../../common/exceptions';

export class ArticlesRepository implements Repository<ArticleDTO> {
  dbClient = prismaClient.article;

  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  findMany = async (options: any): Promise<ArticleDTO[] | undefined> => {
    try {
      // eslint-disable-next-line @typescript-eslint/no-unsafe-assignment
      const { skip, take } = options as { [key: string]: number };
      // eslint-disable-next-line @typescript-eslint/no-explicit-any
      const queryOption: any = {
        skip,
        take,
        orderBy: {
          updatedAt: 'desc',
        },
      };

      // eslint-disable-next-line
      return await this.dbClient.findMany(queryOption);
    } catch (error) {
      if (error instanceof Error) {
        throw new InternalError(error.message);
      }
      return;
    }
  };

  findUnique = async (
    articleId: ArticleDTO['articleId'],
  ): Promise<ArticleDTO | null> => {
    return await this.dbClient.findUnique({
      where: {
        articleId,
      },
    });
  };

  count = async (): Promise<number> => {
    return await this.dbClient.count();
  };
}
