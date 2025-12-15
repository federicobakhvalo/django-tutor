/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './templates/**/*.html',
    './src/**/*.css',
    '../**/templates/**/*.html'
  ],
  darkMode: 'class', // включаем dark mode через класс
  theme: {
    extend: {},
  },
  plugins: [],
}