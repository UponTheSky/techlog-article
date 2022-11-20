import { Article } from '../interfaces/article.interface';

export type ArticleDTO = Omit<Article, 'createdAt' | 'updatedAt'>;
