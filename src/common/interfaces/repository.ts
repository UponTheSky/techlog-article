import { QueryOption, Id, DBClient } from '../types';

export interface Repository<DTO> {
  // CRUD operations
  dbClient: DBClient;

  // Create
  create?(data: Partial<DTO>): DTO;

  // Read
  findMany?: (options?: QueryOption) => Promise<DTO[] | undefined>;
  findById?: (id: Id) => Promise<DTO | null | undefined>;

  // Update
  updateById?: (id: Id) => Promise<DTO | null | undefined>;

  // Delete
  deleteMany?: (options?: QueryOption) => Promise<void>;
  deleteById?: (id: Id) => Promise<void>;
}
