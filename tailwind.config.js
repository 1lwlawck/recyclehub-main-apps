/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: "class",
  mode: "jit",
  purge: [
    "./templates/**/*.html", // Memantau file HTML di folder templates
    "./static/src/**/*.css", // Memantau perubahan di file input.css
    "./static/js/**/*.js", // Memantau perubahan di file JS
    "./**/*.py", // Memantau perubahan pada file Python
  ],
  theme: {
    extend: {
      boxShadow: {
        neo: "8px 8px 0px rgba(0,0,0,1)",
        neoHover: "4px 4px 0px rgba(0,0,0,1)",
      },
      fontFamily: {
        inconsolata: ["Inconsolata", "monospace"],
      },
    },
  },
  plugins: [
    require("flowbite/plugin"),
    require("daisyui"),
    require("flowbite/plugin")({
      charts: true,
    }),
  ],
};
