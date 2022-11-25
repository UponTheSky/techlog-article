import { HttpError } from './httpError';

export class BadRequestError extends HttpError {
  constructor(message: string) {
    super(400, 'BadRequestError');
    this.message = message;
  }
}
