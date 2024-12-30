// Inisialisasi Elemen
const chatList = document.getElementById("chat-list");
const chatMessages = document.getElementById("chat-messages");
const chatForm = document.getElementById("chat-form");
const chatInput = document.getElementById("chat-input");
const chatHeaderName = document.getElementById("chat-name");
const chatHeaderAvatar = document.getElementById("chat-avatar");
const searchInput = document.getElementById("search-chat");

// Variabel Global
let selectedChat = null; // Menyimpan ID penerima
let currentUser = 1; // ID Pengguna saat ini (ganti dengan ID login)

// Fungsi Mengambil Daftar Chat
function fetchChatList() {
  fetch(`/message/fetch/${currentUser}`)
    .then((response) => response.json())
    .then((data) => {
      chatList.innerHTML = ""; // Hapus placeholder
      if (data.success && data.messages.length > 0) {
        const uniqueUsers = new Set();
        data.messages.forEach((msg) => {
          const otherUser = msg.sender_id === currentUser ? msg.receiver_id : msg.sender_id;
          if (!uniqueUsers.has(otherUser)) {
            uniqueUsers.add(otherUser);
            chatList.innerHTML += `
                            <div 
                                class="p-4 flex items-center cursor-pointer hover:bg-blue-300 border-b-4 border-black" 
                                onclick="selectChat(${otherUser})"
                            >
                                <img src="https://via.placeholder.com/40" alt="Avatar" class="w-12 h-12 rounded-lg border-2 border-black" />
                                <div class="ml-4 max-w-full">
                                    <p class="font-bold text-black break-words max-w-full">Pengguna ${otherUser}</p>
                                    <p class="text-sm text-black break-words max-w-full">Klik untuk membuka chat...</p>
                                </div>
                            </div>`;
          }
        });
      } else {
        chatList.innerHTML = `<p class="text-center text-black font-bold">Tidak ada chat tersedia</p>`;
      }
    })
    .catch((error) => {
      console.error("Error fetching chat list:", error);
      chatList.innerHTML = `<p class="text-center text-red-500 font-bold">Gagal memuat daftar chat</p>`;
    });
}

// Fungsi Memilih Chat
function selectChat(userId) {
  selectedChat = userId;
  chatHeaderName.textContent = `Chat dengan Pengguna ${userId}`;
  chatHeaderAvatar.src = "https://via.placeholder.com/40";
  fetchMessages();
}

// Fungsi Mengambil Pesan
function fetchMessages() {
  if (!selectedChat) return;

  fetch(`/message/fetch/${selectedChat}`)
    .then((response) => response.json())
    .then((data) => {
      chatMessages.innerHTML = ""; // Hapus placeholder
      if (data.success && data.messages.length > 0) {
        data.messages.forEach((msg) => {
          const isSender = msg.sender_id === currentUser;
          chatMessages.innerHTML += `
                        <div class="flex ${isSender ? "justify-end" : "justify-start"}">
                            <div class="${isSender ? "bg-green-300 text-black" : "bg-white text-black"} px-4 py-2 rounded-lg shadow-[4px_4px_0px_rgba(0,0,0,1)] border-2 border-black max-w-xs break-words">
                                ${msg.message}
                            </div>
                        </div>`;
        });
      } else {
        chatMessages.innerHTML = `<p class="text-center text-black font-bold">Tidak ada pesan tersedia</p>`;
      }
    })
    .catch((error) => {
      console.error("Error fetching messages:", error);
      chatMessages.innerHTML = `<p class="text-center text-red-500 font-bold">Gagal memuat pesan</p>`;
    });
}

// Fungsi Mengirim Pesan
// Fungsi Mengirim Pesan
function sendMessage(event) {
  event.preventDefault();
  if (!selectedChat || !chatInput.value.trim()) {
    alert("Penerima harus dipilih dan pesan tidak boleh kosong!");
    return;
  }

  const message = chatInput.value.trim();
  chatInput.value = ""; // Kosongkan input setelah pesan dikirim

  // Kirim pesan ke server
  fetch("/message/send", {
    // Endpoint diperbaiki
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      sender_id: currentUser, // ID pengguna saat ini
      receiver_id: selectedChat, // ID penerima yang dipilih
      message: message,
    }),
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.success) {
        fetchMessages(); // Perbarui daftar pesan
      } else {
        alert(`Gagal mengirim pesan: ${data.message}`);
      }
    })
    .catch((error) => {
      console.error("Error sending message:", error);
      alert("Gagal mengirim pesan.");
    });
}

// Fungsi Memperbarui Nama Pengguna dan Avatar di Chat Header setiap detik
function fetchUser(userId) {
  fetch(`/api/messages/get-user/${userId}`)
    .then((response) => response.json())
    .then((data) => {
      if (data.success) {
        // Perbarui nama pengguna dan avatar di chat header
        chatHeaderName.textContent = data.user.nama_user;
        chatHeaderAvatar.src = data.user.avatar;
      } else {
        chatHeaderName.textContent = "Pengguna Tidak Ditemukan";
        chatHeaderAvatar.src = "https://via.placeholder.com/40"; // Avatar default
      }
    })
    .catch((error) => {
      console.error("Error fetching user:", error);
      chatHeaderName.textContent = "Gagal Memuat Nama Pengguna";
    });
}

function selectChat(userId) {
  selectedChat = userId; // Simpan ID pengguna yang dipilih
  fetchUser(userId); // Perbarui header dengan nama dan avatar pengguna
  fetchMessages(); // Ambil pesan untuk pengguna yang dipilih
}

// Fungsi Mencari Chat
function filterChatList() {
  const searchInput = document.getElementById("search-chat").value.toLowerCase();

  fetch(`/api/messages/search-users?query=${searchInput}`)
    .then((response) => response.json())
    .then((data) => {
      if (data.success) {
        chatList.innerHTML = ""; // Kosongkan daftar sebelumnya
        data.users.forEach((user) => {
          chatList.innerHTML += `
              <div 
                class="p-4 flex items-center cursor-pointer hover:bg-blue-300 border-b-4 border-black"
                onclick="selectChat(${user.id})"
              >
                <img src="${user.avatar}" alt="Avatar" class="w-12 h-12 rounded-lg border-2 border-black" />
                <div class="ml-4 max-w-full">
                  <p class="font-bold text-black break-words max-w-full">${user.nama_user}</p>
                </div>
              </div>`;
        });
      } else {
        chatList.innerHTML = `<p class="text-center text-red-500 font-bold">Tidak ada hasil ditemukan</p>`;
      }
    })
    .catch((error) => {
      console.error("Error searching users:", error);
      chatList.innerHTML = `<p class="text-center text-red-500 font-bold">Gagal memuat hasil pencarian</p>`;
    });
}

// Event Listener
searchInput.addEventListener("input", filterChatList);
chatForm.addEventListener("submit", sendMessage);

// Inisialisasi
fetchChatList();
