import dotenv from 'dotenv';

dotenv.config();

export const NODE_ENV = process.env.NODE_ENV || 'development';

export let DATABASE_URL: string;

switch (NODE_ENV) {
  case 'development':
    DATABASE_URL = process.env.DEV_DATABASE_URL as string;
    break;

  case 'test':
    DATABASE_URL = process.env.TEST_DATABASE_URL as string;
    break;

  case 'production':
    DATABASE_URL = process.env.PROD_DATABASE_URL as string;
    break;

  default:
    break;
}
