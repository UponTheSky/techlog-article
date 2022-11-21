import { Article } from '@prisma/client';

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
