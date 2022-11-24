import { Repository } from '../../common/interfaces/repository';
import { LoginDTO, AdminUserDTO } from './admin.dto';
import { prismaClient } from '../../lib/db';

export class AdminLoginRepository implements Repository<LoginDTO> {
  dbClient = prismaClient.adminUser;

  findUnique = async (
    userId: LoginDTO['info']['userId'],
  ): Promise<AdminUserDTO | null> => {
    return await this.dbClient.findUnique({
      where: {
        userId,
      },
    });
  };
}
