import { Repository } from './repository';

export interface ServiceProvider<DTO> {
  readonly repository: Repository<DTO>;
}
