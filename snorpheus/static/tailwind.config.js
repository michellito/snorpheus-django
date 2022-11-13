/** @type {import('tailwindcss').Config} */

module.exports = {
  content: [
    "./**/*.{html,js}",
    "../templates/**/*.{html,js}",
    "./node_modules/flowbite/**/*.js"
  ],
  theme: {
    extend: {
      colors: {
        "dark-purple": "#081A51",
        "light-white": 'rgba(255,255,255,0.18)'
      }
    },
  },
  plugins: [
    require('flowbite/plugin')
  ],
}
