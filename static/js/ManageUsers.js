let currentPage = 1; // Halaman saat ini
const limit = 10; // Jumlah data per halaman
let searchQuery = ""; // Query pencarian
let selectedUserId = null; // ID user yang sedang diedit
let debounceTimeout;

// Fungsi untuk mengambil data user dengan pagination
function fetchUsers(page = 1, search = "") {
  fetch(`/api/users/get-users?page=${page}&limit=${limit}&search=${search}`)
    .then((response) => response.json())
    .then((data) => {
      if (data.success) {
        const tableBody = document.getElementById("user-table-body");
        tableBody.innerHTML = ""; // Bersihkan tabel sebelum mengisi ulang

        if (data.users.length === 0) {
          tableBody.innerHTML = `
            <tr>
              <td colspan="7" class="px-6 py-4 text-center text-gray-500 dark:text-gray-400">
                Data tidak ditemukan
              </td>
            </tr>
          `;
        } else {
          data.users.forEach((user) => {
            const row = document.createElement("tr");
            row.innerHTML = `
              <td class="px-6 py-4 text-center">${user.id}</td>
              <td class="px-6 py-4 text-center">${user.nama_user}</td>
              <td class="px-6 py-4 text-center">${user.email}</td>
              <td class="px-6 py-4 text-center uppercase">${user.role}</td>
              <td class="px-6 py-4 text-center">${
                user.is_verified ? "✔" : "✘"
              }</td>
              <td class="px-6 py-4 text-center">${user.nomor_hp}</td>
              <td class="px-6 py-4 text-center">${user.tanggal_lahir}</td>
              <td class="px-6 py-4 text-center">${user.jenis_kelamin}</td>
              <td class="px-6 py-4 text-center">${user.points}</td>
              <td class="px-6 py-4 text-center">
                <button
                  class="px-4 py-2 bg-blue-500 text-white font-bold rounded shadow-[2px_2px_0px_rgba(0,0,0,1)] hover:bg-blue-400"
                  onclick="openEditModal(${user.id})"
                >
                  Edit
                </button>
                <button
                  class="px-4 py-2 bg-red-500 text-white font-bold rounded shadow-[2px_2px_0px_rgba(0,0,0,1)] hover:bg-red-400"
                  onclick="confirmDelete(${user.id})"
                >
                  Delete
                </button>
              </td>
            `;
            tableBody.appendChild(row);
          });
        }

        // Render tombol pagination
        renderPagination(data.page, data.total, data.limit);
      } else {
        console.error("Error fetching users:", data.message);
      }
    })
    .catch((error) => console.error("Fetch error:", error));
}

// Fungsi untuk membuka modal edit
function openEditModal(userId) {
  selectedUserId = userId;

  // Ambil data user berdasarkan ID
  fetch(`/api/users/get-users?id=${userId}`)
    .then((response) => response.json())
    .then((data) => {
      if (data.success) {
        const user = data.user;

        document.getElementById("edit-nama-user").value = user.nama_user || "";
        document.getElementById("edit-email").value = user.email || "";
        document.getElementById("edit-role").value = user.role || "";
        document.getElementById("edit-nomor-hp").value = user.nomor_hp || "";
        document.getElementById("edit-tanggal-lahir").value = user.tanggal_lahir
          ? new Date(user.tanggal_lahir).toISOString().split("T")[0]
          : "";
        document.getElementById("edit-jenis-kelamin").value =
          user.jenis_kelamin || "";
        document.getElementById("edit-points").value = user.points || 0;

        // Tampilkan modal
        document.getElementById("editUserModal").classList.remove("hidden");
      } else {
        alert("Gagal mengambil data user.");
      }
    })
    .catch((error) => console.error("Fetch error:", error));
}

function saveUserChanges() {
  const nama_user = document.getElementById("edit-nama-user").value.trim();
  const email = document.getElementById("edit-email").value.trim();
  const role = document.getElementById("edit-role").value.trim();
  const points = parseInt(document.getElementById("edit-points").value, 10);
  const nomor_hp = document.getElementById("edit-nomor-hp").value.trim();
  const tanggal_lahir = document
    .getElementById("edit-tanggal-lahir")
    .value.trim();
  const jenis_kelamin = document.getElementById("edit-jenis-kelamin").value;

  // Validasi data
  if (!nama_user || !email || !role || isNaN(points)) {
    alert("Semua field harus diisi dengan benar!");
    return;
  }
  if (!nomor_hp || isNaN(nomor_hp)) {
    alert("Nomor HP harus diisi dengan angka yang valid!");
    return;
  }
  if (!tanggal_lahir) {
    alert("Tanggal lahir harus diisi!");
    return;
  }
  if (!jenis_kelamin) {
    alert("Jenis kelamin harus dipilih!");
    return;
  }

  console.log({
    nama_user,
    email,
    role,
    points,
    nomor_hp,
    tanggal_lahir,
    jenis_kelamin,
  }); // Debugging

  fetch(`/api/users/edit-user/${selectedUserId}`, {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      nama_user,
      email,
      role,
      points,
      nomor_hp,
      tanggal_lahir,
      jenis_kelamin,
    }), // Data JSON
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.success) {
        alert(data.message);
        closeEditModal();
        fetchUsers(currentPage, searchQuery); // Refresh tabel
      } else {
        alert("Gagal memperbarui user: " + data.message);
      }
    })
    .catch((error) => console.error("Update error:", error));
}

function closeEditModal() {
  selectedUserId = null;
  document.getElementById("editUserModal").classList.add("hidden");
}

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
      fetchUsers(page, searchQuery); // Muat data halaman baru
    });

    paginationContainer.appendChild(button);
  }
}

// Fungsi untuk konfirmasi delete
function confirmDelete(userId) {
  if (confirm("Apakah Anda yakin ingin menghapus user ini?")) {
    fetch(`/api/users/delete/${userId}`, { method: "DELETE" })
      .then((response) => response.json())
      .then((data) => {
        if (data.success) {
          alert("User berhasil dihapus.");
          fetchUsers(currentPage, searchQuery); // Refresh tabel
        } else {
          alert("Gagal menghapus user: " + data.message);
        }
      })
      .catch((error) => console.error("Delete error:", error));
  }
}

// Event listener untuk pencarian
document.getElementById("search-input").addEventListener("input", (event) => {
  const searchValue = event.target.value.trim();

  // Tunggu 300ms sebelum memulai pencarian
  clearTimeout(debounceTimeout);
  debounceTimeout = setTimeout(() => {
    searchQuery = searchValue;
    fetchUsers(currentPage, searchQuery);
  }, 300);
});

// Panggil fetchUsers saat halaman dimuat
document.addEventListener("DOMContentLoaded", () => fetchUsers(currentPage));
