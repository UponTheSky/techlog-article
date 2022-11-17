import { PrismaClient } from '@prisma/client';
import { mockDeep, mockReset, DeepMockProxy } from 'jest-mock-extended';

import { prismaClient } from '../../lib/db';

jest.mock('../../lib/db', () => ({
  __esmodule: true,
  prismaClient: mockDeep<PrismaClient>(),
}));

export const prismaClientMock =
  prismaClient as unknown as DeepMockProxy<PrismaClient>;

beforeEach(() => {
  mockReset(prismaClientMock);
});
