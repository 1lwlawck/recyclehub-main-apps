// Referensi elemen
const openModalButton = document.getElementById("openAddArticleModal");
const closeModalButton = document.getElementById("closeAddArticleModal");
const addArticleModal = document.getElementById("addArticleModal");
const addArticleForm = document.getElementById("addArticleForm");
const closeEditModalButton = document.getElementById("closeEditArticleModal");

// Fungsi untuk membuka modal tambah artikel
openModalButton.addEventListener("click", () => {
  addArticleModal.classList.remove("hidden");
});

// Fungsi untuk menutup modal tambah artikel
closeModalButton.addEventListener("click", () => {
  addArticleModal.classList.add("hidden");
});

// Submit form tambah artikel
addArticleForm.addEventListener("submit", async (e) => {
  e.preventDefault();

  const formData = new FormData();
  formData.append("title", document.getElementById("title").value);
  formData.append("author", document.getElementById("author").value);
  formData.append("content", document.getElementById("content").value);

  // Ambil file gambar penulis (profile_picture)
  const profilePicture = document.getElementById("profile_picture").files[0];
  if (profilePicture) {
    formData.append("profile_picture", profilePicture);
  }

  // Ambil file gambar artikel (article_image)
  const articleImage = document.getElementById("article_image").files[0];
  if (articleImage) {
    formData.append("article_image", articleImage); // Tambahkan gambar artikel ke FormData
  }

  try {
    const response = await fetch("/api/articles/new", {
      method: "POST",
      body: formData,
    });

    if (!response.ok) {
      throw new Error("Gagal menambahkan artikel.");
    }

    alert("Artikel berhasil ditambahkan!");
    addArticleModal.classList.add("hidden");
    loadArticles();
  } catch (error) {
    console.error("Error:", error);
    alert(error.message);
  }
});

// Fungsi untuk memuat artikel ke tabel
async function loadArticles() {
  try {
    const response = await fetch("/api/articles/list");
    if (!response.ok) {
      throw new Error("Gagal memuat data artikel.");
    }

    const articles = await response.json();
    const tableBody = document.querySelector("tbody");

    tableBody.innerHTML = "";

    if (articles.length === 0) {
      tableBody.innerHTML = `
        <tr>
          <td colspan="4" class="text-center py-4 text-gray-500">Tidak ada artikel tersedia.</td>
        </tr>
      `;
      return;
    }

    articles.forEach((article) => {
      const row = document.createElement("tr");

      row.innerHTML = `
        <td class="px-6 py-3 border-r-2 border-black text-center">${article.title}</td>
        <td class="px-6 py-3 border-r-2 border-black text-center">${article.author}</td>
        <td class="px-6 py-3 border-r-2 border-black text-center">${article.published_date}</td>
        <td class="px-6 py-3 text-center">
          <button onclick="openEditModal(${article.id})" class="text-yellow-600">Edit</button> |
          <button onclick="deleteArticle(${article.id})" class="text-red-600">Hapus</button>
        </td>
      `;

      tableBody.appendChild(row);
    });
  } catch (error) {
    console.error("Error:", error);
    alert(error.message);
  }
}

// Fungsi untuk membuka modal edit artikel
async function openEditModal(articleId) {
  try {
    const response = await fetch(`/api/articles/get/${articleId}`);
    if (!response.ok) {
      throw new Error("Gagal memuat data artikel.");
    }

    const article = await response.json();

    document.getElementById("editArticleId").value = article.id;
    document.getElementById("editTitle").value = article.title;
    document.getElementById("editAuthor").value = article.author;
    document.getElementById("editContent").value = article.content;

    document.getElementById("editArticleModal").classList.remove("hidden");
  } catch (error) {
    console.error("Error:", error);
    alert(error.message);
  }
}

// Tutup modal edit
closeEditModalButton.addEventListener("click", () => {
  document.getElementById("editArticleModal").classList.add("hidden");
});

// Submit form edit artikel
document
  .getElementById("editArticleForm")
  .addEventListener("submit", async (e) => {
    e.preventDefault();

    const articleId = document.getElementById("editArticleId").value;

    const formData = new FormData();
    formData.append("title", document.getElementById("editTitle").value);
    formData.append("author", document.getElementById("editAuthor").value);
    formData.append("content", document.getElementById("editContent").value);

    try {
      const response = await fetch(`/api/articles/update/${articleId}`, {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        throw new Error("Gagal memperbarui artikel.");
      }

      alert("Artikel berhasil diperbarui.");
      document.getElementById("editArticleModal").classList.add("hidden");
      loadArticles();
    } catch (error) {
      console.error("Error:", error);
      alert(error.message);
    }
  });

async function deleteArticle(articleId) {
  if (!confirm("Apakah Anda yakin ingin menghapus artikel ini?")) {
    return;
  }

  try {
    const response = await fetch(`/api/articles/delete/${articleId}`, {
      method: "DELETE",
    });

    console.log("Response status:", response.status);

    if (!response.ok) {
      const errorData = await response.json();
      console.error("Error data:", errorData);
      throw new Error(errorData.message || "Gagal menghapus artikel.");
    }

    alert("Artikel berhasil dihapus.");
    loadArticles();
  } catch (error) {
    console.error("Error:", error);
    alert(error.message);
  }
}

// Panggil fungsi loadArticles saat halaman dimuat
document.addEventListener("DOMContentLoaded", loadArticles);
