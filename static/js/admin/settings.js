// Fungsi untuk toggle visibilitas password
function togglePasswordVisibility(inputId, button) {
  const input = document.getElementById(inputId);
  if (input.type === "password") {
    input.type = "text";
    button.textContent = "👁️"; // Ikon untuk password terlihat
  } else {
    input.type = "password";
    button.textContent = "🙈"; // Ikon untuk password tersembunyi
  }
}

// Fungsi untuk menyimpan profil (nama dan email)
async function saveProfile() {
  const namaUser = document.getElementById("nama_user").value.trim();
  const email = document.getElementById("email-address").value.trim();

  if (!namaUser || !email) {
    alert("Nama pengguna dan email tidak boleh kosong!");
    return;
  }

  try {
    const response = await fetch("/user/update/0", {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        nama_user: namaUser,
        email: email,
      }),
    });

    const result = await response.json();

    if (result.success) {
      showFlashMessage(
        result.message || "Profile berhasil diperbarui.",
        "success"
      );
    } else {
      showFlashMessage(result.message || "Gagal memperbarui profile.", "error");
    }
  } catch (error) {
    console.error("Error:", error);
    showFlashMessage("Terjadi kesalahan. Silakan coba lagi.", "error");
  }
}

// Fungsi untuk memicu input file
function triggerFileInput() {
  const fileInput = document.getElementById("avatar-file");
  if (fileInput) {
    fileInput.click();
  } else {
    console.error("Input file tidak ditemukan!");
  }
}

// Fungsi untuk mengunggah avatar
async function uploadAvatar(input) {
  const file = input.files[0];
  if (!file) {
    showFlashMessage("Pilih file terlebih dahulu.", "error");
    return;
  }

  const formData = new FormData();
  formData.append("file", file);

  try {
    const response = await fetch("/user/upload-avatar", {
      method: "POST",
      body: formData,
    });

    const result = await response.json();

    if (result.success) {
      // Perbarui avatar
      document.getElementById("avatar-preview").src = `${
        result.avatar_url
      }?t=${new Date().getTime()}`;
      showFlashMessage(
        result.message || "Avatar berhasil diperbarui.",
        "success"
      );
    } else {
      showFlashMessage(result.message || "Gagal memperbarui avatar.", "error");
    }
  } catch (error) {
    console.error("Error:", error);
    showFlashMessage("Terjadi kesalahan saat mengunggah avatar.", "error");
  }
}

// Fungsi untuk mereset avatar ke default
async function resetAvatar() {
  try {
    const response = await fetch("/user/reset-avatar", {
      method: "POST",
    });

    const result = await response.json();

    if (result.success) {
      document.getElementById("avatar-preview").src = `${
        result.avatar_url
      }?t=${Date.now()}`;
      showFlashMessage(result.message || "Avatar berhasil direset.", "success");
    } else {
      showFlashMessage(result.message || "Gagal mereset avatar.", "error");
    }
  } catch (error) {
    console.error("Error:", error);
    showFlashMessage("Terjadi kesalahan saat mereset avatar.", "error");
  }
}

// Fungsi untuk menampilkan pesan flash
function showFlashMessage(message, type) {
  // Hapus flash lama jika ada
  const existingFlash = document.getElementById("flash-message");
  if (existingFlash) {
    existingFlash.remove();
  }

  // Buat elemen flash baru
  const flashMessage = document.createElement("div");
  flashMessage.id = "flash-message";
  flashMessage.className = `fixed top-4 right-4 px-4 py-2 rounded shadow text-white ${
    type === "success" ? "bg-green-500" : "bg-red-500"
  }`;
  flashMessage.innerText = message;

  // Tambahkan ke body
  document.body.appendChild(flashMessage);

  // Hapus pesan setelah 3 detik
  setTimeout(() => {
    if (flashMessage) flashMessage.remove();
  }, 3000);
}
