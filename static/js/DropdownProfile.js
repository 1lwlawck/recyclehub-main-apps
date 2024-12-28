// Fungsi untuk menampilkan atau menyembunyikan dropdown
function toggleDropdown() {
  const dropdown = document.getElementById("dropdown-user");
  if (dropdown) {
    dropdown.classList.toggle("hidden");
  }
}

// Event listener untuk membuka dropdown saat tombol profil diklik
document.addEventListener("DOMContentLoaded", function () {
  const profileButton = document.querySelector(
    "[data-dropdown-toggle='dropdown-user']"
  );

  // Pastikan profileButton dan dropdown tersedia sebelum menambah event listener
  if (profileButton) {
    profileButton.addEventListener("click", function (event) {
      event.stopPropagation(); // Mencegah event klik pada window
      toggleDropdown();
    });
  }

  // Menutup dropdown saat klik di luar area dropdown
  window.addEventListener("click", function (event) {
    const dropdown = document.getElementById("dropdown-user");

    if (dropdown && profileButton) {
      // Periksa apakah klik terjadi di luar dropdown dan tombol profil
      if (
        !dropdown.contains(event.target) &&
        !profileButton.contains(event.target)
      ) {
        dropdown.classList.add("hidden");
      }
    }
  });
});
