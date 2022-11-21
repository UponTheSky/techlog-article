import dotenv from 'dotenv';

dotenv.config();

// server, DB config
export const DATABASE_URL = process.env.DATABASE_URL as string;
export const PORT = process.env.PORT as string;

// main config
export const STATIC_ROOT = 'public';
export const MAIN_ARTICLES_NUMBER = 4;
