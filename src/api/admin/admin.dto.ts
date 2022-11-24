import { AdminUser, Article } from '@prisma/client';

export interface LoginDTO {
  info: {
    userId: string;
    password: string;
  };
}

export type AdminUserDTO = AdminUser;

export type TokenDTO = string;

export type ArticleDTO = Article;

export interface CurrentPageArticlesResponse {
  info: {
    totalArticlesCount: number;
    totalPagesCount: number;
    currentPage: number;
  };
  articles: ArticleDTO[];
}

export type IndividualArticlesResponse = ArticleDTO;
