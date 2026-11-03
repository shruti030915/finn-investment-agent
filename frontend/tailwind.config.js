/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        finn: {
          bg: '#080C14',
          surface: '#0E1524',
          card: '#141E33',
          cardHover: '#1B2844',
          border: '#1F2E4D',
          borderLight: '#2D4168',
          accent: '#38BDF8',
          gold: '#F59E0B',
          gain: '#10B981',
          loss: '#EF4444',
          textMuted: '#8A99AD',
          textSub: '#A8B7CD'
        }
      },
      fontFamily: {
        mono: ['JetBrains Mono', 'Menlo', 'Consolas', 'monospace'],
        sans: ['Inter', '-apple-system', 'BlinkMacSystemFont', 'sans-serif']
      }
    },
  },
  plugins: [],
}
