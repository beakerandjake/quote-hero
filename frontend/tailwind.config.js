/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      colors: {
        wikimedia: "#36c",
        "wikimedia-light": "#447ff5",
      },
    },
  },
  plugins: [],
};
