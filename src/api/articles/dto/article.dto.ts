import { Article } from '../interfaces/article.interface';

export interface ArticleDTO extends Omit<Article, 'createdAt' | 'updatedAt'> {}
