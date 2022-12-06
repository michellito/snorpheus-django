/** @type {import('tailwindcss').Config} */

module.exports = {
  content: [
    "./**/*.{html,js}",
    "../templates/**/*.{html,js}",
    "./node_modules/flowbite/**/*.js"
  ],
  theme: {
    fontFamily: {
      'sans': ['"Segoe UI"', 'ui-sans-serif', 'system-ui'],
      'serif': ['ui-serif', 'Georgia'],
      'mono': ['ui-monospace', 'SFMono-Regular'],
      'display': ['Oswald'],
      'body': ['"Open Sans"'],
    },
    extend: {
      colors: {
        "snorpheus-lt-blue": "#acc4e6",
        "lt-blue": "#d3e2f2",
        "light-white": "rgba(255,255,255,0.18)",
        "snorpheus-yellow": "#faaf47",
        "snorpheus-dk-blue": "#102040",
        "snorpheus-peach": "#fdd19d",
        "dk-gray": "#2a2d30",
        "pink-red": "#ff6666",
        "purple-gray": "#c2c2d6"
      }
    },
  },
  plugins: [
    require('flowbite/plugin')
  ],
}
