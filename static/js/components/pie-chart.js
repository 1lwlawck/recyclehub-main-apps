const ctxPieChart = document.getElementById("pie-chart").getContext("2d");
const pieChart = new Chart(ctxPieChart, {
  type: "pie",
  data: {
    labels: ["Negative", "Positive", "Neutral"], // Labels for the pie chart
    datasets: [
      {
        label: "Dataset",
        data: [300, 50, 100], // Data for each segment of the pie chart
        backgroundColor: ["#ff0000", "#0000ff", "#ffff00"], // Segment colors
        hoverOffset: 4,
      },
    ],
  },
  options: {
    responsive: true,
    plugins: {
      legend: {
        position: "top",
        labels: {
          font: {
            size: 14,
            weight: "bold",
          },
        },
      },
      tooltip: {
        callbacks: {
          label: function (tooltipItem) {
            return tooltipItem.label + ": " + tooltipItem.raw; // Tooltip customization
          },
        },
      },
    },
  },
});
