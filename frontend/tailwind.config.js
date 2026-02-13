/** @type {import('tailwindcss').Config} */
export default {
    content: [
        "./index.html",
        "./src/**/*.{js,ts,jsx,tsx}",
    ],
    theme: {
        extend: {
            colors: {
                // Modern vibrant palette
                background: "#0f0f12",
                surface: "#18181c",
                "surface-light": "#222228",
                "surface-elevated": "#2a2a32",

                // Vibrant blue-violet primary
                primary: {
                    DEFAULT: "#6c5ce7",
                    50: "#f5f3ff",
                    100: "#ede9fe",
                    200: "#ddd6fe",
                    300: "#c4b5fd",
                    400: "#a78bfa",
                    500: "#6c5ce7",
                    600: "#5b4cdb",
                    700: "#4c3fc9",
                    800: "#3d32a8",
                    900: "#312e81",
                },

                // Vibrant cyan accent
                accent: {
                    DEFAULT: "#00d9ff",
                    light: "#5ce1e6",
                    dark: "#00b4d8",
                },

                // Neon green for success
                success: "#00f5a0",
                warning: "#ffc107",
                error: "#ff4757",
                info: "#00d9ff",

                // Text colors
                secondary: "#9ca3af",
                muted: "#6b7280",
            },
            fontFamily: {
                sans: ['Plus Jakarta Sans', 'system-ui', 'sans-serif'],
                display: ['Plus Jakarta Sans', 'system-ui', 'sans-serif'],
                mono: ['Fira Code', 'monospace'],
            },
            backgroundImage: {
                'gradient-primary': 'linear-gradient(135deg, #6c5ce7 0%, #a855f7 100%)',
                'gradient-accent': 'linear-gradient(135deg, #00d9ff 0%, #00f5a0 100%)',
                'gradient-hero': 'linear-gradient(135deg, #6c5ce7 0%, #00d9ff 50%, #00f5a0 100%)',
                'gradient-card': 'linear-gradient(145deg, rgba(108, 92, 231, 0.1) 0%, rgba(0, 217, 255, 0.05) 100%)',
                'gradient-dark': 'radial-gradient(ellipse at top, #1a1a2e 0%, #0f0f12 100%)',
            },
            boxShadow: {
                'glow-primary': '0 0 40px rgba(108, 92, 231, 0.4)',
                'glow-accent': '0 0 40px rgba(0, 217, 255, 0.3)',
                'glow-success': '0 0 30px rgba(0, 245, 160, 0.3)',
                'card': '0 4px 24px rgba(0, 0, 0, 0.4)',
                'card-hover': '0 8px 40px rgba(0, 0, 0, 0.5)',
            },
            animation: {
                'gradient': 'gradient 8s ease infinite',
                'float': 'float 6s ease-in-out infinite',
                'pulse-slow': 'pulse 4s cubic-bezier(0.4, 0, 0.6, 1) infinite',
                'slide-up': 'slideUp 0.5s ease-out',
                'slide-in-right': 'slideInRight 0.5s ease-out',
                'fade-in': 'fadeIn 0.5s ease-out',
                'scale-in': 'scaleIn 0.3s ease-out',
                'bounce-in': 'bounceIn 0.6s cubic-bezier(0.68, -0.55, 0.265, 1.55)',
            },
            keyframes: {
                gradient: {
                    '0%, 100%': { backgroundPosition: '0% 50%' },
                    '50%': { backgroundPosition: '100% 50%' },
                },
                float: {
                    '0%, 100%': { transform: 'translateY(0)' },
                    '50%': { transform: 'translateY(-20px)' },
                },
                slideUp: {
                    '0%': { transform: 'translateY(30px)', opacity: '0' },
                    '100%': { transform: 'translateY(0)', opacity: '1' },
                },
                slideInRight: {
                    '0%': { transform: 'translateX(30px)', opacity: '0' },
                    '100%': { transform: 'translateX(0)', opacity: '1' },
                },
                fadeIn: {
                    '0%': { opacity: '0' },
                    '100%': { opacity: '1' },
                },
                scaleIn: {
                    '0%': { transform: 'scale(0.9)', opacity: '0' },
                    '100%': { transform: 'scale(1)', opacity: '1' },
                },
                bounceIn: {
                    '0%': { transform: 'scale(0.3)', opacity: '0' },
                    '50%': { transform: 'scale(1.05)' },
                    '70%': { transform: 'scale(0.9)' },
                    '100%': { transform: 'scale(1)', opacity: '1' },
                },
            },
            borderRadius: {
                '2xl': '1rem',
                '3xl': '1.5rem',
                '4xl': '2rem',
            },
        },
    },
    plugins: [],
}
