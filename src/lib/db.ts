import { PrismaClient } from '@prisma/client';

// eslint-disable-next-line
export const prismaClient = new PrismaClient();

export type MainDBClient = typeof prismaClient.article;
