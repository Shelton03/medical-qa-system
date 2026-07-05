/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './app/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          DEFAULT: '#4A7C59',
          dark: '#3D6B4A',
          light: '#5A8C69',
        },
        secondary: {
          DEFAULT: '#FAF9F6',
          dark: '#EAE9E6',
          light: '#FFFFFF',
        },
        accent: {
          DEFAULT: '#3D8B8B',
          dark: '#2F7575',
          light: '#4D9B9B',
        },
        text: {
          DEFAULT: '#2D3748',
          light: '#4A5568',
          muted: '#718096',
        },
        error: {
          DEFAULT: '#C85A54',
          dark: '#A84A44',
          light: '#D86A64',
        },
        success: {
          DEFAULT: '#6B8E23',
          dark: '#5B7E13',
          light: '#7B9E33',
        },
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
        heading: ['Inter', 'system-ui', 'sans-serif'],
      },
      screens: {
        'sm': '375px',
        'md': '768px',
        'lg': '1024px',
        'xl': '1440px',
      },
    },
  },
  plugins: [],
}
