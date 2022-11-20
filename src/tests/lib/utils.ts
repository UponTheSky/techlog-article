import { Article } from '../../api/articles/interfaces/article.interface';

export const createFakeArticles = (): Article[] => [
  {
    createdAt: '',
    updatedAt: '',
    title: 'test',
    articleId: '1',
  },
  {
    createdAt: Date.now().toString(),
    updatedAt: Date.now().toString(),
    thumbnail: '',
    title: 'test2',
    excerpt: 'excerpt',
    content: 'content',
    articleId: '2',
  },
];
