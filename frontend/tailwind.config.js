/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,jsx}'],
  theme: {
    extend: {
      fontFamily: { sans: ['Inter', 'sans-serif'] },
      colors: {
        brand: { DEFAULT: '#3B82F6', dark: '#2563EB', light: '#EFF6FF' },
      },
      animation: {
        'pulse-ring': 'pulse-ring 1.4s ease-in-out infinite',
      },
      keyframes: {
        'pulse-ring': {
          '0%, 100%': { boxShadow: '0 0 0 0 rgba(59,130,246,0.4)' },
          '50%':       { boxShadow: '0 0 0 8px rgba(59,130,246,0)' },
        },
      },
    },
  },
  plugins: [],
}
