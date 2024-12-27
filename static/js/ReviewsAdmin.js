// Fungsi untuk menampilkan emoji bintang berdasarkan sentiment
function getStarsBySentiment(sentiment) {
  let starsCount;
  if (sentiment === "positive") {
    starsCount = Math.random() > 0.5 ? 5 : 4; // Random antara 5 atau 4
  } else if (sentiment === "neutral") {
    starsCount = 3;
  } else if (sentiment === "negative") {
    starsCount = Math.random() > 0.5 ? 2 : 1; // Random antara 2 atau 1
  }

  let starsHtml = "🌟".repeat(starsCount); // Ulang emoji 🌟 sesuai jumlah bintang
  return starsHtml;
}

// Fungsi untuk mengambil review dari server
function fetchReviews() {
  fetch("/api/sentiment/reviews") // API endpoint untuk mengambil data review
    .then((response) => response.json())
    .then((data) => {
      const reviewsList = document.getElementById("reviews-list");
      if (!reviewsList) {
        console.error("Element #reviews-list not found!");
        return;
      }

      reviewsList.innerHTML = ""; // Kosongkan daftar sebelum mengisinya

      data.forEach((review) => {
        // Buat elemen <li> baru
        const reviewItem = document.createElement("li");
        reviewItem.classList.add(
          "bg-white",
          "border-4",
          "border-black",
          "rounded-lg",
          "p-6",

          "shadow-[6px_6px_0px_rgba(0,0,0,1)]",
          "hover:shadow-[2px_2px_0px_rgba(0,0,0,1)]",
          "transition"
        );

        // Masukkan konten ke dalam <li>
        const stars = getStarsBySentiment(review.sentiment); // Dapatkan emoji bintang
        reviewItem.innerHTML = `
          <p class="text-gray-800 font-bold"><strong>Review:</strong> ${
            review.text
          }</p>
          <p class="text-gray-500"><strong>Sentiment:</strong> ${
            review.sentiment
          }</p>
          <p class="text-yellow-600 text-lg">${stars}</p>
          <p class="text-gray-400 text-sm">Submitted at: ${new Date(
            review.created_at
          ).toLocaleString()}</p>
        `;

        // Tambahkan <li> ke dalam <ul>
        reviewsList.appendChild(reviewItem);
      });
    })
    .catch((error) => {
      console.error("Error fetching reviews:", error);
    });
}

// Panggil fetchReviews setelah halaman selesai dimuat
document.addEventListener("DOMContentLoaded", function () {
  fetchReviews();
});
