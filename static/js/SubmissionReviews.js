// Fungsi untuk menampilkan modal
function showThankYouModal() {
  const modal = document.getElementById("thank-you-modal");
  if (modal) {
    modal.classList.remove("hidden");
  }
}

// Fungsi untuk menutup modal
function hideThankYouModal() {
  const modal = document.getElementById("thank-you-modal");
  if (modal) {
    modal.classList.add("hidden");
  }
}

// Event listener untuk menutup modal
document
  .getElementById("close-modal")
  .addEventListener("click", hideThankYouModal);

// Event listener untuk form submission
document.getElementById("review-form").addEventListener("submit", function (e) {
  e.preventDefault();
  const reviewText = document.getElementById("reviewText");

  if (!reviewText.value.trim()) {
    alert("Harap masukkan ulasan sebelum mengirim!");
    return;
  }

  fetch("/api/sentiment/analyze", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ text: reviewText.value }),
  })
    .then((response) => {
      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }
      return response.json();
    })
    .then((data) => {
      if (data.error) {
        alert(`Error: ${data.error}`);
        return;
      }

      // Tampilkan modal ucapan terima kasih
      showThankYouModal();

      // Reset textarea
      reviewText.value = "";
    })
    .catch((error) => {
      console.error("Error:", error);
      alert("Terjadi kesalahan. Silakan coba lagi.");
    });
});
