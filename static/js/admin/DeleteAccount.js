document.addEventListener("DOMContentLoaded", () => {
  const deleteAccountButton = document.getElementById("deleteAccountButton");
  const deleteConfirmationModal = document.getElementById(
    "deleteConfirmationModal"
  );
  const cancelDeleteButton = document.getElementById("cancelDeleteButton");
  const confirmDeleteButton = document.getElementById("confirmDeleteButton");

  console.log("deleteAccountButton:", deleteAccountButton);
  console.log("deleteConfirmationModal:", deleteConfirmationModal);
  console.log("cancelDeleteButton:", cancelDeleteButton);
  console.log("confirmDeleteButton:", confirmDeleteButton);

  // Tampilkan modal konfirmasi
  if (deleteAccountButton) {
    deleteAccountButton.addEventListener("click", () => {
      if (deleteConfirmationModal) {
        deleteConfirmationModal.classList.remove("hidden");
      } else {
        console.error("deleteConfirmationModal tidak ditemukan");
      }
    });
  } else {
    console.error("deleteAccountButton tidak ditemukan");
  }

  // Sembunyikan modal saat tombol batal di klik
  if (cancelDeleteButton) {
    cancelDeleteButton.addEventListener("click", () => {
      if (deleteConfirmationModal) {
        deleteConfirmationModal.classList.add("hidden");
      } else {
        console.error("deleteConfirmationModal tidak ditemukan");
      }
    });
  } else {
    console.error("cancelDeleteButton tidak ditemukan");
  }

  // Kirim permintaan DELETE saat tombol konfirmasi di klik
  if (confirmDeleteButton) {
    confirmDeleteButton.addEventListener("click", () => {
      const userId = deleteAccountButton
        ? deleteAccountButton.getAttribute("data-user-id")
        : null;
      if (!userId) {
        console.error("User ID tidak ditemukan");
        return;
      }

      fetch(`/api/users/delete/${userId}`, {
        method: "DELETE",
        headers: {
          "Content-Type": "application/json",
        },
      })
        .then((response) => response.json())
        .then((data) => {
          if (data.success) {
            alert(data.message);
            window.location.href = "/auth/login";
          } else {
            alert(`Gagal menghapus akun: ${data.message}`);
          }
        })
        .catch((error) => {
          console.error("Error:", error);
          alert("Terjadi kesalahan saat menghapus akun.");
        })
        .finally(() => {
          if (deleteConfirmationModal) {
            deleteConfirmationModal.classList.add("hidden");
          }
        });
    });
  } else {
    console.error("confirmDeleteButton tidak ditemukan");
  }
});
