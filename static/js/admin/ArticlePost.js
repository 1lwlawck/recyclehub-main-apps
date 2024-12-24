// Referensi elemen
const openModalButton = document.getElementById("openAddArticleModal");
const closeModalButton = document.getElementById("closeAddArticleModal");
const addArticleModal = document.getElementById("addArticleModal");
const addArticleForm = document.getElementById("addArticleForm");

// Fungsi untuk membuka modal
openModalButton.addEventListener("click", () => {
  addArticleModal.classList.remove("hidden");
});

// Fungsi untuk menutup modal
closeModalButton.addEventListener("click", () => {
  addArticleModal.classList.add("hidden");
});

// Fungsi untuk menangani submit form
addArticleForm.addEventListener("submit", (e) => {
  e.preventDefault();

  const formData = new FormData();
  formData.append("title", document.getElementById("title").value);
  formData.append("author", document.getElementById("author").value);
  formData.append("content", document.getElementById("content").value);
  const profilePicture = document.getElementById("profile_picture").files[0];
  if (profilePicture) {
    formData.append("profile_picture", profilePicture);
  }

  fetch("/articles/new", {
    method: "POST",
    body: formData,
  })
    .then((response) => {
      if (response.ok) {
        alert("Artikel berhasil ditambahkan!");
        addArticleModal.classList.add("hidden");
        loadArticles(); // Perbarui tabel
      } else {
        alert("Gagal menambahkan artikel.");
      }
    })
    .catch((error) => {
      console.error("Error:", error);
    });
});

// Fungsi untuk memuat data artikel dan menampilkannya di tabel
async function loadArticles() {
  try {
    const response = await fetch("/articles/list");

    if (!response.ok) {
      throw new Error("Gagal memuat data artikel.");
    }

    const articles = await response.json();
    const tableBody = document.querySelector("tbody");

    // Kosongkan tabel sebelum menambahkan data baru
    tableBody.innerHTML = "";

    // Jika tidak ada artikel
    if (articles.length === 0) {
      tableBody.innerHTML = `
        <tr>
          <td colspan="5" class="text-center py-4 text-gray-500">Tidak ada artikel tersedia.</td>
        </tr>
      `;
      return;
    }

    // Tambahkan data artikel ke tabel
    articles.forEach((article) => {
      const row = document.createElement("tr");

      row.innerHTML = `
        <td class="px-6 py-3 border-r-2 border-black text-center">${
          article.title
        }</td>
        <td class="px-6 py-3 border-r-2 border-black text-center">${
          article.author
        }</td>
        <td class="px-6 py-3 border-r-2 border-black text-center">${
          article.published_date
        }</td>
        <td class="px-6 py-3 border-r-2 border-black text-center">
          <img src="${
            article.featured_image || "/static/images/default.jpg"
          }" alt="Gambar Artikel" class="w-20 h-20 object-cover">
        </td>
        <td class="px-6 py-3 text-center">
          <a href="/articles/${article.id}" class="text-blue-600">Lihat</a> |
          <a href="/articles/edit/${
            article.id
          }" class="text-yellow-600">Edit</a> |
          <button class="text-red-600" onclick="deleteArticle(${
            article.id
          })">Hapus</button>
        </td>
      `;

      tableBody.appendChild(row);
    });
  } catch (error) {
    console.error("Error:", error);
    alert("Gagal memuat data artikel.");
  }
}

// Fungsi untuk menghapus artikel
async function deleteArticle(articleId) {
  if (!confirm("Apakah Anda yakin ingin menghapus artikel ini?")) {
    return;
  }

  try {
    const response = await fetch(`/articles/delete/${articleId}`, {
      method: "DELETE",
    });

    if (!response.ok) {
      throw new Error("Gagal menghapus artikel.");
    }

    alert("Artikel berhasil dihapus.");
    loadArticles(); // Perbarui tabel
  } catch (error) {
    console.error("Error:", error);
    alert("Terjadi kesalahan saat menghapus artikel.");
  }
}

// Panggil fungsi loadArticles saat halaman dimuat
document.addEventListener("DOMContentLoaded", loadArticles);
