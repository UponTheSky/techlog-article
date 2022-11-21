import { Article } from '@prisma/client';
import { Url } from '../../common/types';

export type ArticleDTO = Article;

export interface MainResponse {
  staticFileUrls: {
    picture: Url;
    shortIntro: Url;
  };
  articles: ArticleDTO[];
}

export type StaticFileList = (keyof MainResponse['staticFileUrls'])[];
