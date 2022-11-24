import { Request, RequestHandler } from 'express';
import jwt from 'jsonwebtoken';
import { UnAuthorizedError } from '../../common/exceptions';
import { SECRET_KEY } from '../config';

const parseTokenFromHeader = (request: Request): string | null => {
  const authorization = request.get('authorization');
  if (authorization && authorization.startsWith('Bearer')) {
    return authorization.replace(/^Bearer /, '');
  }

  return null;
};

export const jwtHandler: RequestHandler = (request, _response, next) => {
  try {
    const token = parseTokenFromHeader(request);
    if (token) {
      const decodedToken = jwt.verify(token, SECRET_KEY) as jwt.JwtPayload;

      if (!decodedToken.userId) {
        throw new UnAuthorizedError('invalid token');
      }

      request.decodedToken = decodedToken;
    }

    next();
  } catch (error) {
    next(error);
  }
};
