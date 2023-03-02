import { HttpError } from './httpError';

export class UnAuthorizedError extends HttpError {
  constructor(message: string) {
    super(401, 'UnAuthorizedError');
    this.message = message;
  }
}
