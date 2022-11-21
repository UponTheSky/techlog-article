import { Article } from '@prisma/client';
import { Url } from '../../common/types';

export type ArticleDTO = Article;

export interface MainResponse {
  mainUrls: {
    picture: Url;
    shortIntro: Url;
  };
  articles: ArticleDTO[];
  menuUrls: {
    me: Url;
    articles: Url;
  };
}

export type StaticFileList = (keyof MainResponse['mainUrls'])[];
export const staticFileList = ['picture', 'shortIntro'] as StaticFileList;
