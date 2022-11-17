import { QueryOption, ItemId, DBClient } from '../types';

export interface Repository<DTO> {
  // CRUD operations
  dbClient: DBClient;

  // Create
  create?(data: Partial<DTO>): Promise<DTO | undefined>;

  // Read
  findMany?: (options?: QueryOption) => Promise<DTO[] | undefined>;
  findById?: (id: ItemId) => Promise<DTO | null | undefined>;

  // Update
  updateById?: (
    id: ItemId,
    data: Partial<DTO>,
  ) => Promise<DTO | null | undefined>;

  // Delete
  deleteMany?: (options?: QueryOption) => Promise<DTO[] | undefined>;
  deleteById?: (id: ItemId) => Promise<DTO | null | undefined>;
}
