import { HttpError } from './httpError';

export class NotFoundError extends HttpError {
  constructor(message: string) {
    super(404, 'NotFoundError');
    this.message = message;
  }
}
