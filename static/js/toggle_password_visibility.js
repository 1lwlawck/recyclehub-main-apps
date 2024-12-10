/**
 * Toggle visibility of password field
 * @param {string} inputId - The ID of the password input field
 * @param {HTMLElement} button - The button element that triggers the toggle
 */
function togglePasswordVisibility(inputId, button) {
  // Ambil elemen input password berdasarkan ID
  const passwordInput = document.getElementById(inputId);

  // Pastikan elemen input ditemukan
  if (!passwordInput) return;

  // Toggle tipe input antara "password" dan "text"
  if (passwordInput.type === "password") {
    passwordInput.type = "text";
    button.innerHTML = "🙉"; // Ubah ikon ke mode visible
  } else {
    passwordInput.type = "password";
    button.innerHTML = "🙈"; // Ubah ikon ke mode hidden
  }
}
