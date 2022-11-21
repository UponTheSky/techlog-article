import { Repository } from '../../common/interfaces/repository';
import { ArticleDTO } from './main.dto';
import { prismaClient, MainDBClient } from '../../lib/db';
import { InternalError } from '../../common/exceptions';
import { MAIN_ARTICLES_NUMBER } from '../../utils/config';

export class MainRepository implements Repository<MainDBClient, ArticleDTO> {
  dbClient = prismaClient.article;

  // eslint-disable-next-line
  findMany = async (monthsBefore: Date) => {
    try {
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
