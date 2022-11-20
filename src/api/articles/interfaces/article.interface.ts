import { Timestamp, UUID } from '../../../common/types';

export interface Article {
  readonly id: number;
  readonly createdAt: Timestamp;
  readonly updatedAt: Timestamp;
  thumbnail: string | null;
  title: string;
  excerpt: string | null;
  content: string | null;
  articleId: UUID;
}
