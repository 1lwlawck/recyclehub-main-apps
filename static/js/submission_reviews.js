// Fungsi untuk menyesuaikan padding berdasarkan tinggi navbar (jika ada)
function adjustPadding() {
  const mainContainer = document.getElementById("main-container");
  const navbar = document.querySelector("nav"); // Pastikan ada elemen <nav> jika digunakan

  if (navbar) {
    // Dapatkan tinggi navbar
    const navbarHeight = navbar.offsetHeight;

    // Atur padding-top kontainer agar tidak tertutup navbar
    mainContainer.style.paddingTop = `${navbarHeight + 16}px`; // Tambahkan margin ekstra jika diperlukan
  }
}

// Panggil fungsi saat halaman dimuat
document.addEventListener("DOMContentLoaded", function () {
  adjustPadding();
});

// Event listener untuk menangani resize
window.addEventListener("resize", adjustPadding);

// Event listener untuk form submission
document.getElementById("review-form").addEventListener("submit", function (e) {
  e.preventDefault();
  const reviewText = document.getElementById("reviewText");

  fetch("/api/sentiment/analyze", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ text: reviewText.value }),
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.error) {
        alert(data.error);
        return;
      }

      // Tampilkan pesan sukses
      alert("Review berhasil ditambahkan!");

      // Reset textarea
      reviewText.value = "";
    })
    .catch((error) => {
      console.error("Error:", error);
      alert("Something went wrong. Please try again.");
    });
});


