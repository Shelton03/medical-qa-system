import type { Config } from 'tailwindcss';

const config: Config = {
  darkMode: ['class'],
  content: [
    './app/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './features/**/*.{js,ts,jsx,tsx,mdx}',
    './providers/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        // Mirage Design System — Primary Palette
        celestialBlue: {
          DEFAULT: '#2563EB',
          50: '#EFF6FF',
          100: '#DBEAFE',
          200: '#BFDBFE',
          300: '#93C5FD',
          400: '#60A5FA',
          500: '#3B82F6',
          600: '#2563EB',
          700: '#1D4ED8',
          800: '#1E40AF',
          900: '#1E3A8A',
        },
        stellarWhite: {
          DEFAULT: '#FAFAF8',
          50: '#FFFFFF',
          100: '#FAFAF8',
          200: '#F5F5F2',
          300: '#E8E5DF',
          400: '#D0CCC6',
        },
        mirageBlack: {
          DEFAULT: '#0A3828',
          50: '#E6F0EC',
          100: '#B3D4C8',
          200: '#80B8A4',
          300: '#4D9C80',
          400: '#1A805C',
          500: '#0A3828',
          600: '#082D20',
          700: '#062218',
          800: '#041710',
          900: '#020B08',
        },
        healthGreen: {
          DEFAULT: '#18A358',
          50: '#ECFDF5',
          100: '#D1FAE5',
          200: '#A7F3D0',
          300: '#6EE7B7',
          400: '#34D399',
          500: '#18A358',
          600: '#059669',
          700: '#047857',
          800: '#065F46',
          900: '#064E3B',
        },
        alertOrange: {
          DEFAULT: '#EA580C',
          50: '#FFF7ED',
          100: '#FFEDD5',
          200: '#FED7AA',
          300: '#FDBA74',
          400: '#FB923C',
          500: '#EA580C',
          600: '#C2410C',
          700: '#9A3412',
          800: '#7C2D12',
          900: '#431407',
        },
        clinicalGrey: {
          DEFAULT: '#6B6760',
          50: '#F8F7F4',
          100: '#F0EEE9',
          200: '#E0DDD6',
          300: '#D0CCC6',
          400: '#A8A39B',
          500: '#6B6760',
          600: '#56534D',
          700: '#4A4742',
          800: '#3E3C37',
          900: '#1a1917',
        },
        deepSpace: {
          DEFAULT: '#0A0A0F',
          50: '#1a1a1f',
          100: '#0A0A0F',
          200: '#08080C',
        },
        // Semantic aliases mapped to the Mirage palette
        primary: {
          DEFAULT: '#0A3828',
          foreground: '#FAFAF8',
        },
        secondary: {
          DEFAULT: '#F0EEE9',
          foreground: '#1a1917',
        },
        accent: {
          DEFAULT: '#2563EB',
          foreground: '#FFFFFF',
        },
        success: {
          DEFAULT: '#18A358',
          foreground: '#FFFFFF',
        },
        warning: {
          DEFAULT: '#EA580C',
          foreground: '#FFFFFF',
        },
        destructive: {
          DEFAULT: '#C2410C',
          foreground: '#FFFFFF',
        },
        muted: {
          DEFAULT: '#F0EEE9',
          foreground: '#6B6760',
        },
        border: '#E0DDD6',
        input: '#D0CCC6',
        ring: '#2563EB',
        background: '#FAFAF8',
        foreground: '#1a1917',
        card: {
          DEFAULT: '#FFFFFF',
          foreground: '#1a1917',
        },
        popover: {
          DEFAULT: '#FFFFFF',
          foreground: '#1a1917',
        },
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', '-apple-system', 'sans-serif'],
        heading: ['Inter', 'system-ui', '-apple-system', 'sans-serif'],
        mono: ['ui-monospace', 'SFMono-Regular', 'Menlo', 'Monaco', 'monospace'],
      },
      fontSize: {
        display: ['2.25rem', { lineHeight: '1.2', fontWeight: '700' }],   // 36px
        'page-title': ['1.75rem', { lineHeight: '1.25', fontWeight: '700' }], // 28px
        'section-title': ['1.375rem', { lineHeight: '1.3', fontWeight: '600' }], // 22px
        'card-title': ['1.125rem', { lineHeight: '1.4', fontWeight: '600' }], // 18px
        body: ['1rem', { lineHeight: '1.6', fontWeight: '400' }],        // 16px
        caption: ['0.75rem', { lineHeight: '1.5', fontWeight: '400' }],   // 12px
        micro: ['0.625rem', { lineHeight: '1.4', fontWeight: '500', letterSpacing: '0.04em' }], // 10px
      },
      spacing: {
        '1': '4px',
        '2': '8px',
        '3': '12px',
        '4': '16px',
        '5': '20px',
        '6': '24px',
        '8': '32px',
        '10': '40px',
        '12': '48px',
        '16': '64px',
      },
      borderRadius: {
        button: '9999px',
        card: '16px',
        sheet: '32px',
        input: '16px',
        dialog: '24px',
        'phone-frame': '44px',
      },
      boxShadow: {
        'elevation-1': '0 1px 3px rgba(10, 10, 15, 0.08), 0 1px 2px rgba(10, 10, 15, 0.06)',
        'elevation-2': '0 4px 6px rgba(10, 10, 15, 0.08), 0 2px 4px rgba(10, 10, 15, 0.06)',
        'elevation-3': '0 10px 15px rgba(10, 10, 15, 0.08), 0 4px 6px rgba(10, 10, 15, 0.06)',
        'elevation-4': '0 20px 25px rgba(10, 10, 15, 0.08), 0 8px 10px rgba(10, 10, 15, 0.06)',
        'elevation-5': '0 25px 50px rgba(10, 10, 15, 0.12)',
        'phone': '0 25px 50px -12px rgba(10, 10, 15, 0.25), 0 0 0 1px rgba(10, 10, 15, 0.05)',
      },
      backdropBlur: {
        glass: '20px',
      },
      transitionTimingFunction: {
        'spring': 'cubic-bezier(0.34, 1.56, 0.64, 1)',
        'ease-standard': 'cubic-bezier(0.4, 0, 0.2, 1)',
        'ease-enter': 'cubic-bezier(0, 0, 0.2, 1)',
        'ease-exit': 'cubic-bezier(0.4, 0, 1, 1)',
      },
      transitionDuration: {
        'instant': '100ms',
        'fast': '200ms',
        'standard': '300ms',
        'slow': '450ms',
        'background': '800ms',
      },
      keyframes: {
        'fade-in': {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
        'slide-up': {
          '0%': { transform: 'translateY(24px)', opacity: '0' },
          '100%': { transform: 'translateY(0)', opacity: '1' },
        },
        'slide-down': {
          '0%': { transform: 'translateY(-24px)', opacity: '0' },
          '100%': { transform: 'translateY(0)', opacity: '1' },
        },
        'scale-in': {
          '0%': { transform: 'scale(0.96)', opacity: '0' },
          '100%': { transform: 'scale(1)', opacity: '1' },
        },
        shimmer: {
          '0%': { backgroundPosition: '-200% 0' },
          '100%': { backgroundPosition: '200% 0' },
        },
      },
      animation: {
        'fade-in': 'fade-in 300ms ease-standard forwards',
        'slide-up': 'slide-up 300ms ease-standard forwards',
        'slide-down': 'slide-down 300ms ease-standard forwards',
        'scale-in': 'scale-in 300ms ease-standard forwards',
        'shimmer': 'shimmer 1.5s infinite linear',
      },
      screens: {
        'xs': '375px',
        'sm': '640px',
        'md': '768px',
        'lg': '1024px',
        'xl': '1280px',
        '2xl': '1440px',
      },
    },
  },
  plugins: [],
};

export default config;
