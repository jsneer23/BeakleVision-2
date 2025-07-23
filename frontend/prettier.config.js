export default {
  semi: true,
  singleQuote: true,
  trailingComma: 'all',
  tabWidth: 2,
  plugins: [
    '@trivago/prettier-plugin-sort-imports',
    'prettier-plugin-tailwindcss',
    'prettier-plugin-classnames',
    'prettier-plugin-merge',
  ],
  tailwindFunctions: ['clsx', 'cn', 'cva'],
  customFunctions: ['clsx', 'cn', 'cva'],
  importOrder: ['^@/(.*)$', '^~icons/(.*)$', '^~/(.*)$', '^[./]'],
  importOrderSeparation: true,
  importOrderSortSpecifiers: true,
  tailwindStylesheet: './src/tailwind.css',
};