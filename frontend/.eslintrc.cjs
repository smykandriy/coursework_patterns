module.exports = {
  env: {
    browser: true,
    es2021: true
  },
  extends: [
    'eslint:recommended',
    'plugin:react/recommended',
    'plugin:@typescript-eslint/recommended',
    'plugin:react-hooks/recommended',
    'prettier'
  ],
  parser: '@typescript-eslint/parser',
  parserOptions: {
    ecmaVersion: 'latest',
    sourceType: 'module'
  },
  plugins: ['react', '@typescript-eslint', 'react-refresh'],
  rules: {
    'react/react-in-jsx-scope': 'off',
    'react-refresh/only-export-components': 'warn'
  },
  settings: {
    react: {
      version: 'detect'
    }
  }
}
