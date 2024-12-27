// Pastikan plugin ChartDataLabels terdaftar
Chart.register(ChartDataLabels);

// Elemen canvas
const ctxPieChart = document.getElementById("pie-chart").getContext("2d");

// Inisialisasi pie chart
const pieChart = new Chart(ctxPieChart, {
  type: "pie",
  data: {
    labels: ["Negative", "Neutral", "Positive"],
    datasets: [
      {
        label: "Sentiment Distribution",
        data: [0, 0, 0], // Data awal
        backgroundColor: ["#ff0000", "#ffff00", "#0000ff"], // Warna setiap segmen
        hoverOffset: 4,
      },
    ],
  },
  options: {
    responsive: true,
    plugins: {
      // Konfigurasi legend
      legend: {
        position: "top",
        labels: {
          font: {
            size: 14,
            weight: "bold",
          },
        },
      },
      // Konfigurasi tooltip
      tooltip: {
        callbacks: {
          label: function (tooltipItem) {
            const total = tooltipItem.dataset.data.reduce(
              (acc, value) => acc + value,
              0
            );
            const percentage = ((tooltipItem.raw / total) * 100).toFixed(2); // Hitung persentase
            return `${tooltipItem.label}: ${tooltipItem.raw} (${percentage}%)`;
          },
        },
      },
      // Konfigurasi datalabels
      datalabels: {
        formatter: (value, context) => {
          const total = context.dataset.data.reduce((acc, val) => acc + val, 0);
          const percentage = ((value / total) * 100).toFixed(2);
          return `${percentage}%`; // Tampilkan persentase
        },
        color: "#fff", // Warna label
        font: {
          size: 14, // Ukuran font
          weight: "bold",
        },
      },
    },
  },
});

async function fetchSentimentData() {
  try {
    const response = await fetch("/api/sentiment/sentiments");
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const sentimentData = await response.json();
    console.log("Data dari API:", sentimentData); // Debugging

    // Pastikan data tidak undefined atau null
    if (!sentimentData) {
      console.error("Sentiment data is empty or undefined!");
      return;
    }

    // Update data pie chart
    pieChart.data.datasets[0].data = [
      sentimentData.Negative || 0,
      sentimentData.Neutral || 0,
      sentimentData.Positive || 0,
    ];

    // Render ulang chart dengan data baru
    pieChart.update();
  } catch (error) {
    console.error("Error fetching sentiment data:", error);
  }
}

// Panggil fetchSentimentData setelah halaman selesai dimuat
window.addEventListener("load", fetchSentimentData);
