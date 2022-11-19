import dotenv from 'dotenv';

dotenv.config();

export const DATABASE_URL = process.env.DATABASE_URL as string;
export const NODE_ENV = process.env.NODE_ENV || 'development';
