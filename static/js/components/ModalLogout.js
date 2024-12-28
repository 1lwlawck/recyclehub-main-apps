// Fungsi untuk menampilkan modal
function showModal(modalId) {
  const modal = document.getElementById(modalId);
  if (modal) {
    modal.classList.remove("hidden"); // Tampilkan modal dengan menghapus kelas "hidden"
    modal.classList.add("flex"); // Tambahkan kelas "flex" untuk memusatkan modal
  }
}

// Fungsi untuk menyembunyikan modal
function hideModal(modalId) {
  const modal = document.getElementById(modalId);
  if (modal) {
    modal.classList.add("hidden"); // Sembunyikan modal dengan menambahkan kelas "hidden"
    modal.classList.remove("flex"); // Hapus kelas "flex" untuk memusatkan modal
  }
}

// Event listener untuk tombol yang membuka modal
document.addEventListener("DOMContentLoaded", function () {
  // Tombol Log Out
  const logoutButton = document.querySelector(
    "[data-modal-target='logout-modal']"
  );
  if (logoutButton) {
    logoutButton.addEventListener("click", function (event) {
      event.preventDefault(); // Mencegah perilaku default dari link
      showModal("logout-modal"); // Tampilkan modal
    });
  }

  // Tombol di dalam modal untuk menyembunyikan modal
  const closeButtons = document.querySelectorAll(
    "[data-modal-hide='logout-modal']"
  );
  closeButtons.forEach((button) => {
    button.addEventListener("click", function () {
      hideModal("logout-modal"); // Sembunyikan modal
    });
  });

  // Menyembunyikan modal ketika pengguna mengklik di luar area modal
  const modal = document.getElementById("logout-modal");
  if (modal) {
    modal.addEventListener("click", function (event) {
      if (event.target === modal) {
        hideModal("logout-modal");
      }
    });
  }
});
