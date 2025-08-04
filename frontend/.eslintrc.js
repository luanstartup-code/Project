module.exports = {
  extends: [
    'react-app',
    'react-app/jest'
  ],
  rules: {
    'no-restricted-globals': [
      'error',
      {
        name: 'confirm',
        message: 'Use window.confirm instead.'
      }
    ],
    'no-unused-vars': 'warn',
    'no-console': 'off',
    'react-hooks/exhaustive-deps': 'off'
  }
};