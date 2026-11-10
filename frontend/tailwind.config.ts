import type { Config } from "tailwindcss";

export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  darkMode: "class",
  theme: {
    extend: {
      colors: {
        canvas: "#000000",
        surface: {
          DEFAULT: "#000000",
          50: "#27272A",
          100: "#18181B",
          200: "#121214",
          300: "#0C0C0E",
          400: "#060607",
          500: "#000000",
        },
        border: {
          subtle: "#18181B",
          muted: "#27272A",
          active: "#3F3F46",
        },
        brand: {
          red: "#E11D48",
          emerald: "#10B981",
          cyan: "#0EA5E9",
        },
      },
      fontFamily: {
        sans: ["Inter", "-apple-system", "BlinkMacSystemFont", "Segoe UI", "sans-serif"],
        display: ["Inter", "sans-serif"],
        mono: ["JetBrains Mono", "SF Mono", "Consolas", "monospace"],
      },
    },
  },
  plugins: [],
} satisfies Config;
