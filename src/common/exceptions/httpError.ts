export class HttpError extends Error {
  name: string;
  status: number;

  constructor(status: number, name: string) {
    super();
    this.status = status;
    this.name = name;
  }
}
