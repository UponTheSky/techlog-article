import { HttpError } from './httpError';

export class InternalError extends HttpError {
  constructor(message: string) {
    super(500, 'InternalError');
    this.message = message;
  }
}
