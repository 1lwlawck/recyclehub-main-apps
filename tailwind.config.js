/** @type {import('tailwindcss').Config} */
module.exports = {
  mode: "jit",
  purge: [
    "./templates/**/*.html", // Memantau file HTML di folder templates
    "./static/src/**/*.css", // Memantau perubahan di file input.css
    "./static/js/**/*.js", // Memantau perubahan di file JS
    "./**/*.py", // Memantau perubahan pada file Python
  ],
  theme: {
    extend: {
      fontFamily: {
        inconsolata: ["Inconsolata", "monospace"],
      },
    },
  },
  plugins: [require("flowbite/plugin")],
};
