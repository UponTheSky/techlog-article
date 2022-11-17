import { Request, RequestHandler } from 'express';
import jwt, { JwtPayload } from 'jsonwebtoken';
import { UnAuthorizedError } from '../../common/exceptions';
import { SECRET_KEY } from '../config';

declare global {
  namespace Express {
    interface Request {
      decodedToken?: JwtPayload;
    }
  }
}

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

    if (token && !request.url.startsWith('/api/admin/login')) {
      jwt.verify(token, SECRET_KEY, (err, decodedToken) => {
        if (!decodedToken || !(decodedToken as jwt.JwtPayload).userId) {
          throw new UnAuthorizedError(`invalid token: ${err?.message ?? ''}`);
        }

        request.decodedToken = decodedToken as jwt.JwtPayload;
      });
    }
    next();
  } catch (error) {
    next(error);
  }
};

export const jwtAdminArticlesHandler: RequestHandler = (
  request,
  _response,
  next,
) => {
  try {
    if (
      request.url.startsWith('/api/admin/articles') &&
      !request.decodedToken
    ) {
      throw new UnAuthorizedError(
        'You must be authenticated in order to get access to this page',
      );
    }
    next();
  } catch (error) {
    next(error);
  }
};
