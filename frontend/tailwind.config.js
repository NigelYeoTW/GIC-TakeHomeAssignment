/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  // disable preflight to prevent conflicts with Ant Design's base styles
  corePlugins: {
    preflight: false,
  },
};
