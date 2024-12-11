let currentPage = 1; // Halaman saat ini
const limit = 10; // Jumlah data per halaman
let searchQuery = ""; // Query pencarian
let debounceTimeout = null;
let selectedUserId = null; // Untuk menyimpan ID user yang akan dihapus

// Fungsi fetchUsers untuk memuat data berdasarkan halaman dan pencarian
function fetchUsers(page = 1, search = "") {
  fetch(`/user/get-users?page=${page}&limit=${limit}&search=${search}`)
    .then((response) => response.json())
    .then((data) => {
      if (data.success) {
        const tableBody = document.getElementById("user-table-body");
        tableBody.innerHTML = ""; // Bersihkan tabel sebelum mengisi ulang

        if (data.users.length === 0) {
          // Jika tidak ada data, tampilkan pesan "Data tidak ditemukan"
          const noDataRow = document.createElement("tr");
          noDataRow.innerHTML = `
            <td colspan="8" class="px-6 py-4 text-center text-gray-500 dark:text-gray-400">
              Data tidak ditemukan
            </td>
          `;
          tableBody.appendChild(noDataRow);
        } else {
          data.users.forEach((user) => {
            const row = document.createElement("tr");
            row.innerHTML = `
              <td class="px-6 py-4 text-center">${user.id}</td>
              <td class="px-6 py-4 text-center" contenteditable="true" data-field="nama_user" data-id="${
                user.id
              }">
                ${user.nama_user}
              </td>
              <td class="px-6 py-4 text-center" contenteditable="true" data-field="email" data-id="${
                user.id
              }">
                ${user.email}
              </td>
              <td class="px-6 py-4 text-center" contenteditable="true" data-field="role" data-id="${
                user.id
              }">
                ${user.role}
              </td>
              <td class="px-6 py-4 text-center">${
                user.is_verified ? "✔" : "✘"
              }</td>
              
              <td class="px-6 py-4 text-center" contenteditable="true" data-field="points" data-id="${
                user.id
              }">
                ${user.points}
              </td>
              <td class="px-6 py-4 text-center">
                <button class="bg-gradient-to-r from-blue-500 to-purple-500 text-white px-3 py-1 rounded" onclick="showDeleteModal(${
                  user.id
                })">
                  Delete
                </button>
              </td>
            `;
            tableBody.appendChild(row);
          });

          // Tambahkan event listener pada sel yang bisa diedit
          enableInlineEditing();
        }

        // Tampilkan pagination
        renderPagination(data.page, data.total, data.limit);
      } else {
        console.error("Error fetching users:", data.message);
      }
    })
    .catch((error) => console.error("Fetch error:", error));
}

// Fungsi untuk mengaktifkan inline editing
function enableInlineEditing() {
  const editableCells = document.querySelectorAll("[contenteditable=true]");

  editableCells.forEach((cell) => {
    cell.addEventListener("blur", () => {
      const field = cell.getAttribute("data-field");
      const id = cell.getAttribute("data-id");
      const newValue = cell.textContent.trim();

      if (!newValue) {
        alert("Field tidak boleh kosong!");
        fetchUsers(currentPage, searchQuery); // Refresh tabel jika data kosong
        return;
      }

      // Kirim perubahan ke server
      updateUser(id, field, newValue);
    });
  });
}

// Fungsi untuk memperbarui data user di server
function updateUser(userId, field, value) {
  fetch(`/user/update/${userId}`, {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      [field]: field === "points" ? parseInt(value) : value,
    }),
  })
    .then((response) => response.json())
    .then((data) => {
      if (!data.success) {
        alert("Gagal memperbarui data: " + data.message);
        fetchUsers(currentPage, searchQuery); // Refresh tabel untuk mengembalikan data asli
      } else {
        alert("Data berhasil diperbarui!");
      }
    })
    .catch((error) => {
      console.error("Update error:", error);
    });
}

// Fungsi untuk menampilkan modal delete
function showDeleteModal(userId) {
  selectedUserId = userId; // Simpan ID user yang dipilih
  const modal = document.getElementById("deleteModal");
  const modalText = document.getElementById("deleteModalText");

  // Update teks modal dengan ID user
  modalText.textContent = `Apakah Anda yakin ingin menghapus user dengan ID ${userId}?`;

  // Tampilkan modal
  modal.classList.remove("hidden");
}

// Fungsi untuk menutup modal delete
function closeDeleteModal() {
  selectedUserId = null; // Reset ID user
  const modal = document.getElementById("deleteModal");
  modal.classList.add("hidden");
}

/// Fungsi untuk menampilkan pesan alert di sebelah kanan
function showAlert(message, type = "danger") {
  const alertContainer = document.createElement("div");
  alertContainer.className = `fixed mt-20 top-4 right-4 z-50 flex items-center p-4 text-sm rounded-lg shadow-lg ${
    type === "danger"
      ? "text-red-800 bg-red-50 dark:bg-gray-800 dark:text-red-400"
      : "text-green-800 bg-green-50 dark:bg-gray-800 dark:text-green-400"
  }`;
  alertContainer.role = "alert";

  alertContainer.innerHTML = `
      <svg class="flex-shrink-0 inline w-4 h-4 mr-3" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 20 20">
        <path d="M10 .5a9.5 9.5 0 1 0 9.5 9.5A9.51 9.51 0 0 0 10 .5ZM9.5 4a1.5 1.5 0 1 1 0 3 1.5 1.5 0 0 1 0-3ZM12 15H8a1 1 0 0 1 0-2h1v-3H8a1 1 0 0 1 0-2h2a1 1 0 1 1 1 1v4h1a1 1 0 0 1 0 2Z"/>
      </svg>
      <div>
        <span class="font-medium">${
          type === "danger" ? "Error:" : "Success:"
        }</span> ${message}
      </div>
    `;

  // Tambahkan alert ke body, sehingga selalu muncul di layar
  document.body.appendChild(alertContainer);

  // Hilangkan alert setelah 3 detik
  setTimeout(() => {
    alertContainer.remove();
  }, 3000);
}

// Fungsi untuk menghapus user
function confirmDelete() {
  if (selectedUserId) {
    fetch(`/user/delete/${selectedUserId}`, { method: "DELETE" })
      .then((response) => response.json())
      .then((data) => {
        if (data.success) {
          showAlert("User berhasil dihapus!", "success");
          fetchUsers(currentPage, searchQuery); // Refresh tabel
        } else {
          showAlert("Gagal menghapus user: " + data.message, "danger");
        }
        closeDeleteModal(); // Tutup modal
      })
      .catch((error) => {
        console.error("Delete error:", error);
        showAlert("Terjadi kesalahan. Coba lagi nanti.", "danger");
        closeDeleteModal();
      });
  }
}

// Tambahkan event listener ke tombol modal
document
  .getElementById("cancelDelete")
  .addEventListener("click", closeDeleteModal);
document
  .getElementById("confirmDelete")
  .addEventListener("click", confirmDelete);

// Fungsi untuk menampilkan tombol pagination
function renderPagination(currentPage, totalUsers, limit) {
  const paginationContainer = document.getElementById("pagination");
  paginationContainer.innerHTML = ""; // Bersihkan pagination

  const totalPages = Math.ceil(totalUsers / limit);

  for (let page = 1; page <= totalPages; page++) {
    const button = document.createElement("button");
    button.textContent = page;
    button.className = `px-3 py-1 mx-1 ${
      page === currentPage
        ? "bg-blue-500 text-white"
        : "bg-gray-200 dark:bg-gray-700 text-gray-700 dark:text-gray-200"
    } rounded hover:bg-blue-300 dark:hover:bg-gray-500`;

    button.addEventListener("click", () => {
      currentPage = page;
      fetchUsers(page, searchQuery); // Muat data halaman baru dengan pencarian
    });

    paginationContainer.appendChild(button);
  }
}

// Event listener untuk pencarian dengan debounce
document.getElementById("search-input").addEventListener("input", (event) => {
  const searchValue = event.target.value.trim();
  clearTimeout(debounceTimeout); // Hapus timeout sebelumnya

  // Atur timeout baru
  debounceTimeout = setTimeout(() => {
    searchQuery = searchValue;
    currentPage = 1; // Reset ke halaman pertama
    fetchUsers(currentPage, searchQuery); // Muat ulang tabel dengan pencarian
  }, 300); // Tunggu 300ms sebelum melakukan request
});

// Panggil fetchUsers saat halaman dimuat
document.addEventListener("DOMContentLoaded", () => fetchUsers(currentPage));
