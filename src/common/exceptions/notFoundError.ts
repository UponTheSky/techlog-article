export class NotFoundError extends Error {
  name: string;
  status: number;

  constructor(message: string) {
    super();
    this.status = 404;
    this.name = 'NotFoundError';
    this.message = message;
  }
}
