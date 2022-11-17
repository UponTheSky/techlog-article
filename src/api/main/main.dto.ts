import { Article } from '@prisma/client';
import { Url } from '../../common/types';

export type ArticleDTO = Article;

export interface MainResponse {
  mainInfos: {
    picture: Url;
    shortIntro: string;
  };
  articles: ArticleDTO[];
}

export type StaticFileList = (keyof MainResponse['mainInfos'])[];
export const staticFileList = ['picture', 'shortIntro'] as StaticFileList;
