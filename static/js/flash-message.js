function handleFlashMessages() {
  // Ambil semua elemen dengan class flash-message
  const flashMessages = document.querySelectorAll(".flash-message");

  // Atur timer untuk menyembunyikan setiap flash message setelah 5 detik
  flashMessages.forEach((message) => {
    setTimeout(() => {
      message.style.transition = "opacity 0.5s ease";
      message.style.opacity = "0"; // Fade out pesan flash
      setTimeout(() => message.remove(), 500); // Hapus elemen setelah animasi selesai
    }, 5000); // 5 detik
  });
}

// Jalankan fungsi handleFlashMessages saat halaman dimuat
document.addEventListener("DOMContentLoaded", handleFlashMessages);
