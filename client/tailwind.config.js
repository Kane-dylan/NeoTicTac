/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {},
  },
  plugins: [],
  // Enable Tailwind 4 features
  future: {
    hoverOnlyWhenSupported: true,
  },
  // Tailwind 4 uses JIT (Just-In-Time) mode by default
  mode: "jit",
};
