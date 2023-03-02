import { Repository } from '../../common/interfaces/repository';
import { ArticleDTO } from './main.dto';
import { prismaClient } from '../../lib/db';
import { InternalError } from '../../common/exceptions';
import { MAIN_ARTICLES_NUMBER } from '../../utils/config';

export class MainRepository implements Repository<ArticleDTO> {
  dbClient = prismaClient.article;

  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  findMany = async (monthsBefore: Date) => {
    try {
      // eslint-disable-next-line @typescript-eslint/no-explicit-any
      const queryOption: any = {
        take: MAIN_ARTICLES_NUMBER,
        where: {
          updatedAt: {
            gt: monthsBefore,
          },
        },
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
}
