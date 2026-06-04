import type { Config } from 'jest';

const config: Config = {
  preset: 'ts-jest',
  testEnvironment: 'node',
  roots: ['<rootDir>/clockwords/tests'],
  testMatch: ['**/*.test.ts'],
};

export default config;
