function getGreeting() {
  const now = new Date();
  const hour = now.getHours();
  let greeting = "";

  if (hour >= 5 && hour < 12) {
    greeting = "Selamat Pagi! 🌅";
  } else if (hour >= 12 && hour < 15) {
    greeting = "Selamat Siang! ☀️";
  } else if (hour >= 15 && hour < 18) {
    greeting = "Selamat Sore! 🌤️";
  } else {
    greeting = "Selamat Malam! 🌙";
  }

  return greeting;
}

// Update teks di dalam card
document.getElementById("greeting").textContent = getGreeting();
