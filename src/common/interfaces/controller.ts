import { Router } from 'express';
import { Url } from '../types';
import { ServiceProvider } from './service';

export interface Controller<T> {
  readonly path: Url;
  router: Router;
  readonly serviceProvider: ServiceProvider<T>;

  exportRouter(): Router;
  initRouter(): void;
}
