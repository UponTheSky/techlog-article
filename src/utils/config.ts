import dotenv from 'dotenv';

dotenv.config();

// server, DB config
export const DATABASE_URL = process.env.DATABASE_URL as string;
export const PORT = process.env.PORT as string;

// api/main, api/me config
export const STATIC_ROOT = 'public';
export const MAIN_ARTICLES_NUMBER = 4;

// api/articles config
export const ARTICLES_ARTICLES_NUMBER = 6;
export const ARTICLES_DEFAULT_CURRENT_PAGE = 0;

// api/admin config
export const ADMIN_ARTICLES_NUMBER = 10;
export const ADMIN_DEFAULT_CURRENT_PAGE = 0;
