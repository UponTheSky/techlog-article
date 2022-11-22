export class InternalError extends Error {
  name: string;
  status: number;

  constructor(message: string) {
    super();
    this.status = 500;
    this.name = 'InternalError';
    this.message = message;
  }
}
