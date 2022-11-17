module.exports = {
  extends: [
    'eslint:recommended', 
    'plugin:@typescript-eslint/recommended',
    'plugin:@typescript-eslint/recommended-requiring-type-checking',
    'prettier'
  ],
  parser: '@typescript-eslint/parser',
  parserOptions: {
    tsconfigRootDir: __dirname,
    project: 'tsconfig.json',
    sourceType: 'module'
  },
  overrides: [
    {
      files: [`${__dirname}/.eslintrc.js`],
      parserOptions: {
        project: null
      }
    }
  ],
  plugins: ['@typescript-eslint'],
  root: true,
  env: {
    node: true
  }
}
