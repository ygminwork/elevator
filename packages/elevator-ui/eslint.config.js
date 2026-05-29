import js from '@eslint/js'
import globals from 'globals'
import reactHooks from 'eslint-plugin-react-hooks'
import reactRefresh from 'eslint-plugin-react-refresh'
import tseslint from 'typescript-eslint'
import prettierConfig from "eslint-config-prettier";
import prettierPlugin from "eslint-plugin-prettier";
import { defineConfig, globalIgnores } from 'eslint/config'
import perfectionist from 'eslint-plugin-perfectionist';

export default defineConfig([
  globalIgnores(['dist']),
  {
    files: ['**/*.{ts,tsx}'],
    extends: [
      js.configs.recommended,
      tseslint.configs.recommended,
      reactHooks.configs.flat.recommended,
      reactRefresh.configs.vite,
      {
        plugins: {
          perfectionist,
        },
        rules: {
          'perfectionist/sort-enums': ['error', { type: 'alphabetical', ignoreCase: false }],
          'perfectionist/sort-imports': ['error', { type: 'alphabetical', newlinesBetween: 1, ignoreCase: false }],
          'perfectionist/sort-objects': ['error', { type: 'alphabetical', ignoreCase: false }],
        },
      },
      {
        plugins: {
          prettier: prettierPlugin,
        },
        rules: {
          "prettier/prettier": "error",
        },
      },
      prettierConfig,
    ],
    languageOptions: {
      globals: globals.browser,
    },
  },
])
