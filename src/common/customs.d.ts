import { Request } from 'express';
import { JwtPayload } from 'jsonwebtoken';

declare global {
  namespace Express {
    export interface Request {
      decodedToken?: JwtPayload;
    }
  }
}
