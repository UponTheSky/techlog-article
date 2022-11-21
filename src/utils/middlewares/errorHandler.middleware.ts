import { RequestHandler, ErrorRequestHandler } from 'express';

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
  _response,
  next,
): void => {
  if (error instanceof Error) {
    logger.error(error);
  }

  // example code
  /**
   * if (error.name === 'notFoundError') {
   *  response.status(404).json({
   *   error: 'data not found'
   *  })
   * }
   */

  next(error);
};
