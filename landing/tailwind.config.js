module.exports = {
  darkMode: 'class',
  content: [
  "./build/**/*.{html,js}"
  ],
  theme: {
    extend: {
      animation: {
        'spin-slow': 'spin 10s linear infinite',
      }
    },
  },
  plugins: [],
}