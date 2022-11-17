/** @type {import('ts-jest').JestConfigWithTsJest} */
module.exports = {
  verbose: true,
  preset: 'ts-jest',
  testEnvironment: 'node',
  maxWorkers: 1,
  testPathIgnorePatterns: ['/node_modules/', '/dist/']
};