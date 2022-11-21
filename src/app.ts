import express from 'express';
import morgan from 'morgan';
import path from 'path';

import { mainController } from './api';

import {
  unknownEndpoint,
  errorHandler,
} from './utils/middlewares/errorHandler.middleware';

// app initialization
export const app = express();

// add basic middlewares
app.use(express.json());
app.use(morgan('combined'));
app.use('/public', express.static(path.join(__dirname, '../public')));

// add routes
app.use(mainController.exportRouter());

// add error handlers
app.use(unknownEndpoint);
app.use(errorHandler);
