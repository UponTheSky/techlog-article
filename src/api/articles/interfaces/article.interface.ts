import { Timestamp, UUID } from '../../../common/types';

export interface Article {
  readonly createdAt: Timestamp;
  readonly updatedAt: Timestamp;
  thumbnail?: string;
  title: string;
  excerpt?: string;
  content?: string;
  articleId: UUID;
}
