/** @type {import('tailwindcss').Config} */
export default {
    content: [
        "./index.html",
        "./src/**/*.{js,ts,jsx,tsx}",
    ],
    theme: {
        extend: {
            colors: {
                // Base colors
                background: "#0a0b0f",
                surface: "#12141a",
                "surface-light": "#1a1d25",

                // Primary gradient colors
                primary: {
                    DEFAULT: "#6366f1",
                    50: "#eef2ff",
                    100: "#e0e7ff",
                    200: "#c7d2fe",
                    300: "#a5b4fc",
                    400: "#818cf8",
                    500: "#6366f1",
                    600: "#4f46e5",
                    700: "#4338ca",
                    800: "#3730a3",
                    900: "#312e81",
                },

                // Accent colors
                accent: {
                    DEFAULT: "#8b5cf6",
                    light: "#a78bfa",
                    dark: "#7c3aed",
                },

                // Semantic colors
                secondary: "#64748b",
                success: "#10b981",
                warning: "#f59e0b",
                error: "#ef4444",

                // Glass effect colors
                glass: {
                    DEFAULT: "rgba(255, 255, 255, 0.05)",
                    light: "rgba(255, 255, 255, 0.1)",
                    border: "rgba(255, 255, 255, 0.1)",
                },
            },
            fontFamily: {
                sans: ['Inter', 'system-ui', 'sans-serif'],
            },
            backgroundImage: {
                // Gradient backgrounds
                'gradient-radial': 'radial-gradient(var(--tw-gradient-stops))',
                'gradient-primary': 'linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%)',
                'gradient-accent': 'linear-gradient(135deg, #8b5cf6 0%, #ec4899 100%)',
                'gradient-dark': 'linear-gradient(180deg, #0a0b0f 0%, #12141a 100%)',
                'gradient-glass': 'linear-gradient(135deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0.05) 100%)',
                'gradient-glow': 'radial-gradient(circle at center, rgba(99,102,241,0.15) 0%, transparent 70%)',
            },
            boxShadow: {
                'glass': '0 8px 32px rgba(0, 0, 0, 0.3)',
                'glass-lg': '0 16px 48px rgba(0, 0, 0, 0.4)',
                'glow': '0 0 20px rgba(99, 102, 241, 0.3)',
                'glow-lg': '0 0 40px rgba(99, 102, 241, 0.4)',
                'glow-accent': '0 0 20px rgba(139, 92, 246, 0.3)',
            },
            backdropBlur: {
                'xs': '2px',
            },
            animation: {
                'float': 'float 6s ease-in-out infinite',
                'pulse-slow': 'pulse 3s ease-in-out infinite',
                'glow': 'glow 2s ease-in-out infinite alternate',
                'slide-up': 'slideUp 0.5s ease-out',
                'fade-in': 'fadeIn 0.5s ease-out',
                'spin-slow': 'spin 3s linear infinite',
            },
            keyframes: {
                float: {
                    '0%, 100%': { transform: 'translateY(0)' },
                    '50%': { transform: 'translateY(-10px)' },
                },
                glow: {
                    '0%': { opacity: '0.5' },
                    '100%': { opacity: '1' },
                },
                slideUp: {
                    '0%': { transform: 'translateY(20px)', opacity: '0' },
                    '100%': { transform: 'translateY(0)', opacity: '1' },
                },
                fadeIn: {
                    '0%': { opacity: '0' },
                    '100%': { opacity: '1' },
                },
            },
            borderRadius: {
                '2xl': '1rem',
                '3xl': '1.5rem',
            },
        },
    },
    plugins: [],
}
