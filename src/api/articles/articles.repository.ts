import { v4 as uuid } from 'uuid';

import { Repository } from '../../common/interfaces/repository';
import { ArticleDTO } from './articles.dto';
import { prismaClient } from '../../lib/db';
import { BadRequestError, InternalError } from '../../common/exceptions';
import { Prisma } from '@prisma/client';

export class ArticlesRepository implements Repository<ArticleDTO> {
  dbClient = prismaClient.article;

  // READ

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
    id: ArticleDTO['articleId'],
  ): Promise<ArticleDTO | null> => {
    return await this.dbClient.findUnique({
      where: {
        articleId: id,
      },
    });
  };

  count = async (): Promise<number> => {
    return await this.dbClient.count();
  };

  // UPDATE
  updateById = async (
    id: ArticleDTO['articleId'],
    data: Partial<ArticleDTO>,
  ): Promise<ArticleDTO | null | undefined> => {
    try {
      return await this.dbClient.update({
        where: {
          articleId: id,
        },
        data: {
          ...data,
          updatedAt: new Date(Date.now()),
        },
      });
    } catch (error) {
      if (error instanceof Prisma.NotFoundError) {
        return null;
      }
      return;
    }
  };

  // CREATE
  create = async (data: Partial<ArticleDTO>): Promise<ArticleDTO> => {
    const { thumbnail, title, excerpt, content } = data;

    if (!title || title.length === 0) {
      throw new BadRequestError('an article must have its title');
    }

    return await this.dbClient.create({
      data: {
        createdAt: new Date(Date.now()),
        updatedAt: new Date(Date.now()),
        thumbnail,
        title,
        excerpt,
        content,
        articleId: uuid(),
      },
    });
  };

  // DELETE
  deleteById = async (
    id: ArticleDTO['articleId'],
  ): Promise<ArticleDTO | null | undefined> => {
    try {
      return await this.dbClient.delete({
        where: {
          articleId: id,
        },
      });
    } catch (error) {
      if (error instanceof Prisma.NotFoundError) {
        return null;
      }
      return;
    }
  };
}
