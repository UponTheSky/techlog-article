export class BadRequestError extends Error {
  name: string;
  status: number;

  constructor(message: string) {
    super();
    this.status = 400;
    this.name = 'BadRequestError';
    this.message = message;
  }
}
