// URL API
const API_URL = "/api/alamat";

// Fungsi untuk Fetch Data Alamat
async function fetchAlamatData() {
  try {
    const response = await fetch(API_URL);
    if (!response.ok) {
      throw new Error(`Error: ${response.status}`);
    }

    const data = await response.json();
    renderAlamatTable(data);
  } catch (error) {
    console.error("Error fetching data:", error);
    alert("Gagal memuat data alamat.");
  }
}

// Fungsi untuk Render Data ke Tabel
function renderAlamatTable(data) {
  const tableBody = document.getElementById("alamat-table-body");

  // Kosongkan tabel sebelum render
  tableBody.innerHTML = "";

  // Loop melalui data dan tambahkan baris ke tabel
  data.forEach((alamat) => {
    const row = `
        <tr>
            <td class="px-6 py-4 text-center border-r-2 border-black">${
              alamat.id
            }</td>
            <td class="px-6 py-4 text-center border-r-2 border-black">${
              alamat.user_id
            }</td>
            <td class="px-6 py-4 text-center border-r-2 border-black">${
              alamat.provinsi
            }</td>
            <td class="px-6 py-4 text-center border-r-2 border-black">${
              alamat.kabupaten_kota
            }</td>
            <td class="px-6 py-4 text-center border-r-2 border-black">${
              alamat.kecamatan
            }</td>
            <td class="px-6 py-4 text-center border-r-2 border-black">${
              alamat.desa
            }</td>
            <td class="px-6 py-4 text-center border-r-2 border-black">${
              alamat.kode_pos
            }</td>
            <td class="px-6 py-4 text-center border-r-2 border-black">${
              alamat.latitude || "-"
            }</td>
            <td class="px-6 py-4 text-center border-r-2 border-black">${
              alamat.longitude || "-"
            }</td>
            <td class="px-6 py-4 text-center border-r-2 border-black">${
              alamat.alamat_lengkap
            }</td>
            <td class="px-6 py-4 text-center">
                <button class="mb-2 edit-btn bg-yellow-400 text-black px-4 py-2 rounded-md shadow-md" data-id="${
                  alamat.id
                }">Edit</button>
                <button class="delete-btn bg-red-400 text-white px-4 py-2 rounded-md shadow-md" data-id="${
                  alamat.id
                }">Delete</button>
            </td>
        </tr>
      `;
    tableBody.insertAdjacentHTML("beforeend", row);
  });

  // Tambahkan event listener untuk tombol aksi
  addActionListeners();
}

// Fungsi untuk Delete Data
async function deleteAlamat(id) {
  try {
    const response = await fetch(`${API_URL}/${id}`, {
      method: "DELETE",
    });

    if (!response.ok) {
      throw new Error(`Error: ${response.status}`);
    }

    closeDeleteModal();
    openSuccessModal("Data berhasil dihapus!");
    fetchAlamatData(); // Refresh tabel
  } catch (error) {
    console.error("Error deleting data:", error);
    alert("Terjadi kesalahan saat menghapus data.");
  }
}

// Fungsi untuk Update Data
async function updateAlamat(id, updatedData) {
  try {
    const response = await fetch(`${API_URL}/${id}`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(updatedData),
    });

    if (!response.ok) {
      throw new Error(`Error: ${response.status}`);
    }

    closeEditAlamatModal();
    openEditSuccessModal(); // Tampilkan modal sukses
    fetchAlamatData(); // Refresh tabel
  } catch (error) {
    console.error("Error updating data:", error);
    alert("Terjadi kesalahan saat memperbarui data.");
  }
}

// Tambahkan Event Listener untuk tombol aksi
function addActionListeners() {
  // Tombol Delete
  document.querySelectorAll(".delete-btn").forEach((button) => {
    button.addEventListener("click", (event) => {
      const id = event.target.getAttribute("data-id");
      openDeleteModal(id);
    });
  });

  // Tombol Edit
  document.querySelectorAll(".edit-btn").forEach((button) => {
    button.addEventListener("click", async (event) => {
      const id = event.target.getAttribute("data-id");
      try {
        const response = await fetch(`${API_URL}/${id}`);
        if (!response.ok) throw new Error("Gagal memuat data untuk edit.");

        const data = await response.json();
        openEditAlamatModal(data);
      } catch (error) {
        console.error("Error loading edit data:", error);
        alert("Terjadi kesalahan saat memuat data untuk diedit.");
      }
    });
  });
}

// Modal Konfirmasi Delete
const deleteModal = document.getElementById("deleteModal");
let idToDelete = null;

function openDeleteModal(id) {
  idToDelete = id;
  deleteModal.classList.remove("hidden");
}

function closeDeleteModal() {
  deleteModal.classList.add("hidden");
}

document
  .getElementById("cancelDelete")
  .addEventListener("click", closeDeleteModal);
document.getElementById("confirmDelete").addEventListener("click", () => {
  if (idToDelete) {
    deleteAlamat(idToDelete);
  }
});

// Modal Success
const successModal = document.getElementById("successModal");

function openSuccessModal(message) {
  document.getElementById("successModalText").textContent = message;
  successModal.classList.remove("hidden");
}

function closeSuccessModal() {
  successModal.classList.add("hidden");
}

document
  .getElementById("closeSuccessModal")
  .addEventListener("click", closeSuccessModal);

// Modal Edit Alamat
const editAlamatModal = document.getElementById("editAlamatModal");

function openEditAlamatModal(data) {
  document.getElementById("edit-provinsi").value = data.provinsi || "";
  document.getElementById("edit-kabupaten-kota").value =
    data.kabupaten_kota || "";
  document.getElementById("edit-kecamatan").value = data.kecamatan || "";
  document.getElementById("edit-desa").value = data.desa || "";
  document.getElementById("edit-kode-pos").value = data.kode_pos || "";
  document.getElementById("edit-latitude").value = data.latitude || "";
  document.getElementById("edit-longitude").value = data.longitude || "";
  document.getElementById("edit-alamat-lengkap").value =
    data.alamat_lengkap || "";

  // Simpan ID yang sedang diedit
  editAlamatModal.dataset.id = data.id;
  editAlamatModal.classList.remove("hidden");
}

function closeEditAlamatModal() {
  editAlamatModal.classList.add("hidden");
}

document.getElementById("editAlamatForm").addEventListener("submit", (e) => {
  e.preventDefault();

  const id = editAlamatModal.dataset.id;
  const updatedData = {
    provinsi: document.getElementById("edit-provinsi").value,
    kabupaten_kota: document.getElementById("edit-kabupaten-kota").value,
    kecamatan: document.getElementById("edit-kecamatan").value,
    desa: document.getElementById("edit-desa").value,
    kode_pos: document.getElementById("edit-kode-pos").value,
    latitude:
      parseFloat(document.getElementById("edit-latitude").value) || null,
    longitude:
      parseFloat(document.getElementById("edit-longitude").value) || null,
    alamat_lengkap: document.getElementById("edit-alamat-lengkap").value,
  };

  updateAlamat(id, updatedData);
});

// Modal Edit Berhasil
const editSuccessModal = document.getElementById("editSuccessModal");

function openEditSuccessModal() {
  editSuccessModal.classList.remove("hidden");
}

function closeEditSuccessModal() {
  editSuccessModal.classList.add("hidden");
}

document
  .getElementById("closeEditSuccessModal")
  .addEventListener("click", closeEditSuccessModal);

// Panggil fungsi Fetch Data saat halaman dimuat
document.addEventListener("DOMContentLoaded", fetchAlamatData);
