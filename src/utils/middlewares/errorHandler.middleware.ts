import { RequestHandler, ErrorRequestHandler } from 'express';

import * as logger from '../logger';

export const unknownEndpoint: RequestHandler = (_request, response, _next) => {
  response.status(404).json({
    error: 'unknown endpoint',
  });
  return;
};

export const errorHandler: ErrorRequestHandler = (
  error,
  request,
  response,
  next,
) => {
  logger.error(error.message);

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
