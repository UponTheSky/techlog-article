import bcrypt from 'bcrypt';
import jwt from 'jsonwebtoken';
import { ServiceProvider } from '../../common/interfaces/service';
import { LoginDTO, TokenDTO } from './admin.dto';
import { AdminLoginRepository } from './admin.login.repository';
import { UnAuthorizedError } from '../../common/exceptions';
import { SECRET_KEY } from '../../utils/config';

export class AdminLoginServiceProvider implements ServiceProvider<TokenDTO> {
  repository = new AdminLoginRepository();

  validateUserInfo = async ({
    info: { userId, password },
  }: LoginDTO): Promise<TokenDTO> => {
    const adminUser = await this.repository.findUnique(userId);
    const passwordCorrect =
      adminUser && (await bcrypt.compare(password, adminUser.passwordHash));

    if (!adminUser || !passwordCorrect) {
      throw new UnAuthorizedError('either user id or password is invalid');
    }

    const token = jwt.sign(
      {
        userId,
        id: adminUser.id,
      },
      SECRET_KEY,
    );

    return token;
  };
}
