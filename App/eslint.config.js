// eslint.config.js - https://eslint.org/docs/latest/use/configure/language-options
export default [
  {
    languageOptions: {
      ecmaVersion: 2024,
      sourceType: 'module',
      parserOptions: {
        ecmaFeatures: {
          jsx: true,
        },
      },
    },
  },
];
