/** @type {import('tailwindcss').Config} */
module.exports = {
    content: [
        "./index.html",
        "./src/**/*.{js,ts,jsx,tsx}",
    ],
    theme: {
        extend: {
            colors: {
                burgundy: {
                    DEFAULT: '#800020',
                    light: '#A01535',
                    dark: '#5C0016',
                },
                gold: {
                    DEFAULT: '#FFD700',
                    dim: '#C5A000',
                },
                dark: {
                    bg: '#121212',
                    card: '#1E1E1E',
                }
            },
            fontFamily: {
                serif: ['"Playfair Display"', 'serif'],
                sans: ['Inter', 'sans-serif'],
            }
        },
    },
    plugins: [],
}
