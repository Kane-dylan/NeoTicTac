/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      colors: {
        // Retro Arcade Neon Colors
        neon: {
          green: "#00ff41",
          pink: "#ff0080",
          cyan: "#00ffff",
          purple: "#8000ff",
          yellow: "#ffff00",
          orange: "#ff4000",
        },
        cyber: {
          black: "#0a0a0a",
          dark: "#1a1a2e",
          darker: "#16213e",
          blue: "#0f3460",
          purple: "#533483",
        },
        grid: {
          line: "#00ff4120",
          glow: "#00ff4140",
        },
        text: {
          primary: "#ffffff",
          secondary: "#00ff41",
          muted: "#808080",
          inverse: "#0a0a0a",
          neon: "#00ffff",
        },
        background: {
          primary: "#0a0a0a",
          secondary: "#1a1a2e",
          tertiary: "#16213e",
          dark: "#000000",
          card: "rgba(26, 26, 46, 0.8)",
        },
        primary: {
          DEFAULT: "#00ff41",
          hover: "#00cc33",
          glow: "rgba(0, 255, 65, 0.5)",
        },
        secondary: {
          DEFAULT: "#ff0080",
          hover: "#cc0066",
          glow: "rgba(255, 0, 128, 0.5)",
        },
        accent: {
          success: "#00ff41",
          warning: "#ffff00",
          error: "#ff0080",
          info: "#00ffff",
        },
        border: {
          light: "#00ff4140",
          medium: "#00ff4160",
          dark: "#00ff4180",
          neon: "#00ff41",
        },
      },
      fontFamily: {
        mono: ["JetBrains Mono", "Fira Code", "Courier New", "monospace"],
        pixel: ["Press Start 2P", "monospace"],
      },
      boxShadow: {
        neon: "0 0 10px currentColor, 0 0 20px currentColor, 0 0 30px currentColor",
        "neon-sm": "0 0 5px currentColor, 0 0 10px currentColor",
        "neon-lg":
          "0 0 20px currentColor, 0 0 40px currentColor, 0 0 60px currentColor",
        inner: "inset 0 2px 4px 0 rgba(0, 0, 0, 0.3)",
      },
      animation: {
        "neon-pulse": "neon-pulse 2s ease-in-out infinite alternate",
        "neon-flicker": "neon-flicker 0.15s ease-in-out infinite alternate",
        "scan-line": "scan-line 2s linear infinite",
        "float-up": "float-up 3s ease-in-out infinite",
        "glow-rotate": "glow-rotate 4s linear infinite",
      },
      keyframes: {
        "neon-pulse": {
          "0%": {
            textShadow:
              "0 0 5px currentColor, 0 0 10px currentColor, 0 0 15px currentColor",
          },
          "100%": {
            textShadow:
              "0 0 2px currentColor, 0 0 5px currentColor, 0 0 8px currentColor",
          },
        },
        "neon-flicker": {
          "0%, 100%": { opacity: "1" },
          "50%": { opacity: "0.8" },
        },
        "scan-line": {
          "0%": { transform: "translateY(-100%)" },
          "100%": { transform: "translateY(100vh)" },
        },
        "float-up": {
          "0%, 100%": { transform: "translateY(0px)" },
          "50%": { transform: "translateY(-10px)" },
        },
        "glow-rotate": {
          "0%": { transform: "rotate(0deg)" },
          "100%": { transform: "rotate(360deg)" },
        },
      },
    },
  },
  plugins: [],
  // Tailwind 4 configuration
  future: {
    hoverOnlyWhenSupported: true,
  },
  mode: "jit",
};
