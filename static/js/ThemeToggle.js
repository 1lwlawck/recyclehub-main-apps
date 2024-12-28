document.addEventListener("DOMContentLoaded", () => {
  const themeToggle = document.getElementById("theme-toggle");
  const darkIcon = document.getElementById("theme-toggle-dark-icon");
  const lightIcon = document.getElementById("theme-toggle-light-icon");
  let isToggling = false; // Mencegah double-click

  // Inisialisasi tema berdasarkan localStorage atau preferensi sistem
  if (
    localStorage.getItem("theme") === "dark" ||
    (!("theme" in localStorage) &&
      window.matchMedia("(prefers-color-scheme: dark)").matches)
  ) {
    document.documentElement.classList.add("dark");
    lightIcon.classList.remove("hidden");
    darkIcon.classList.add("hidden");
  } else {
    document.documentElement.classList.remove("dark");
    darkIcon.classList.remove("hidden");
    lightIcon.classList.add("hidden");
  }

  // Event listener untuk toggle tema
  themeToggle.addEventListener("click", (event) => {
    event.stopPropagation();

    if (isToggling) return; // Cegah toggle jika sedang dalam proses
    isToggling = true;

    const isDarkMode = document.documentElement.classList.contains("dark");

    if (isDarkMode) {
      document.documentElement.classList.remove("dark");
      localStorage.setItem("theme", "light");
      darkIcon.classList.remove("hidden");
      lightIcon.classList.add("hidden");
      console.log("Switched to light mode");
    } else {
      document.documentElement.classList.add("dark");
      localStorage.setItem("theme", "dark");
      darkIcon.classList.add("hidden");
      lightIcon.classList.remove("hidden");
      console.log("Switched to dark mode");
    }

    // Beri waktu sebelum toggle diizinkan kembali
    setTimeout(() => {
      isToggling = false;
    }, 300); // Adjust delay sesuai kebutuhan
  });
});
