import globals from 'globals';
import pluginJs from '@eslint/js';
import pluginReact from 'eslint-plugin-react';

export default [
  { files: ['**/*.{js,mjs,cjs,jsx}'] },
  pluginJs.configs.recommended,
  pluginReact.configs.flat.recommended,
  pluginReact.configs.flat['jsx-runtime'],
  {
    languageOptions: {
      ecmaVersion: 'latest',
      globals: globals.browser
    }
  },
  {
    settings: {
      react: {
        version: 'detect'
      }
    }
  },
  {
    rules: {
      'no-unused-vars': 'warn',
      'no-undef': 'warn',

      // Stylistic Issues
      'indent': ['warn', 2, {
        'SwitchCase': 1,
        'ignoredNodes': ['TemplateLiteral']
      }],
      'quotes': ['warn', 'single', {
        'allowTemplateLiterals': true
      }],
      'no-irregular-whitespace': 'warn',
      'brace-style': ['warn'],
      'no-multiple-empty-lines': ['warn', {
        'max': 1
      }],
      'no-trailing-spaces': ['warn'],
      'no-unneeded-ternary': ['warn'],
      'comma-spacing': ['warn'],
      'comma-style': ['warn'],
      'comma-dangle': ['warn'],
      'eol-last': ['warn'],
      'jsx-quotes': ['warn', 'prefer-double'],
      'operator-linebreak': ['warn', 'before'],

      // Best Practices
      'eqeqeq': ['error', 'always', {
        'null': 'ignore'
      }],
      'no-multi-spaces': ['warn', {
        'ignoreEOLComments': true,
        'exceptions': {
          'Property': false
        }
      }],
      'key-spacing': ['warn', {
        'beforeColon': false,
        'afterColon': true
      }],
      'object-curly-spacing': ['warn', 'always'],
      'curly': ['warn']
    }
  }
];
