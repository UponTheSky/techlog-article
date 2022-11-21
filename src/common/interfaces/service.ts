import { Repository } from './repository';

export interface ServiceProvider<DBClient, DTO> {
  readonly repository: Repository<DBClient, DTO>;
}
