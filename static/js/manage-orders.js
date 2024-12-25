// URL API untuk mengelola orders
const API_URL = "/orders";

// Elemen DOM
const orderTableBody = document.getElementById("order-table-body");
const searchInput = document.getElementById("search-input");
const deleteOrderModal = document.getElementById("deleteOrderModal");
const cancelDeleteOrder = document.getElementById("cancelDeleteOrder");
const confirmDeleteOrder = document.getElementById("confirmDeleteOrder");
let selectedOrderId = null;

// Fungsi untuk mengambil data orders dari API
async function fetchOrders(query = "") {
  try {
    const response = await fetch(`${API_URL}?search=${query}`);
    const data = await response.json();
    renderOrders(data);
  } catch (error) {
    console.error("Error fetching orders:", error);
  }
}

// Fungsi untuk merender orders ke tabel
function renderOrders(orders) {
  orderTableBody.innerHTML = "";

  if (orders.length === 0) {
    orderTableBody.innerHTML = `
      <tr>
        <td colspan="7" class="text-center py-4">Tidak ada data orders.</td>
      </tr>
    `;
    return;
  }

  orders.forEach((order) => {
    const row = document.createElement("tr");
    row.classList.add("border-b");

    row.innerHTML = `
      <td class="px-6 py-3 text-center">${order.id_order}</td>
      <td class="px-6 py-3 text-center">${order.nama_user}</td>
      <td class="px-6 py-3 text-center">${order.tanggal_pengantaran}</td>
      <td class="px-6 py-3 text-center">${order.waktu_pengantaran}</td>
      <td class="px-6 py-3 text-center">${order.status_order}</td>
      <td class="px-6 py-3 text-center">
        ${order.details
          .map(
            (detail) => `
              <div>
                <p>${detail.jenis_sampah} - ${detail.perkiraan_berat} kg</p>
                <img src="${detail.foto_sampah}" alt="Foto Sampah" class="w-16 h-16">
              </div>
            `
          )
          .join("")}
      </td>
      <td class="px-6 py-3 text-center">
        <button class="text-red-500 hover:underline" onclick="showDeleteModal(${order.id_order})">Hapus</button>
      </td>
    `;
    orderTableBody.appendChild(row);
  });
}

// Fungsi untuk menampilkan modal konfirmasi delete
function showDeleteModal(orderId) {
  selectedOrderId = orderId;
  deleteOrderModal.classList.remove("hidden");
}

// Fungsi untuk menyembunyikan modal konfirmasi delete
function hideDeleteModal() {
  selectedOrderId = null;
  deleteOrderModal.classList.add("hidden");
}

// Fungsi untuk menghapus order
async function deleteOrder() {
  if (!selectedOrderId) return;

  try {
    const response = await fetch(`${API_URL}/${selectedOrderId}`, {
      method: "DELETE",
    });

    if (response.ok) {
      hideDeleteModal();
      fetchOrders(searchInput.value); // Refresh data
      alert("Order berhasil dihapus.");
    } else {
      console.error("Error deleting order:", await response.text());
      alert("Gagal menghapus order.");
    }
  } catch (error) {
    console.error("Error deleting order:", error);
    alert("Terjadi kesalahan saat menghapus order.");
  }
}

// Event Listener untuk pencarian
searchInput.addEventListener("input", (e) => {
  fetchOrders(e.target.value);
});

// Event Listener untuk tombol batal hapus
cancelDeleteOrder.addEventListener("click", hideDeleteModal);

// Event Listener untuk tombol konfirmasi hapus
confirmDeleteOrder.addEventListener("click", deleteOrder);

// Inisialisasi data orders saat halaman dimuat
fetchOrders();
