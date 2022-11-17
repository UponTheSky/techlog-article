import { RequestHandler, ErrorRequestHandler } from 'express';
import { HttpError } from '../../common/exceptions/httpError';

import * as logger from '../logger';

export const unknownEndpoint: RequestHandler = (_request, response): void => {
  response.status(404).json({
    error: 'unknown endpoint',
  });
  return;
};

export const errorHandler: ErrorRequestHandler = (
  error,
  _request,
  response,
  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  next,
): void => {
  // eslint-disable-next-line @typescript-eslint/no-unsafe-argument
  logger.error(error);

  error instanceof HttpError
    ? response.status(error.status).json({
        error: `${error.name}: ${error.message}`,
      })
    : response.status(500).json({
        error: 'internal server error',
      });

  next(error);
};
