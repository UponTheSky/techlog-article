export class UnAuthorizedError extends Error {
  name: string;
  status: number;

  constructor(message: string) {
    super();
    this.status = 401;
    this.name = 'UnAuthorizedError';
    this.message = message;
  }
}
