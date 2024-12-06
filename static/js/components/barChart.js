window.addEventListener("load", () => {
  // Membuat chart bar
  (function () {
    var options = {
      chart: {
        type: "bar",
        height: "100%", // Membuat chart menyesuaikan dengan tinggi card
        toolbar: {
          show: false,
        },
        zoom: {
          enabled: false,
        },
      },
      series: [
        {
          name: "Sales",
          data: [
            23000, 44000, 55000, 57000, 56000, 61000, 58000, 63000, 60000,
            66000, 34000, 78000,
          ], // Data Sales
        },
      ],
      plotOptions: {
        bar: {
          horizontal: false,
          columnWidth: "16px",
          borderRadius: 0,
        },
      },
      legend: {
        show: false,
      },
      dataLabels: {
        enabled: false,
      },
      stroke: {
        show: true,
        width: 8,
        colors: ["transparent"],
      },
      xaxis: {
        categories: [
          "January",
          "February",
          "March",
          "April",
          "May",
          "June",
          "July",
          "August",
          "September",
          "October",
          "November",
          "December",
        ], // Labels for X axis (months)
        axisBorder: {
          show: false,
        },
        axisTicks: {
          show: false,
        },
        crosshairs: {
          show: false,
        },
        labels: {
          style: {
            colors: "#9ca3af",
            fontSize: "13px",
            fontFamily: "Inter, ui-sans-serif",
            fontWeight: 400,
          },
          offsetX: -2,
          formatter: (title) => title.slice(0, 3), // Abbreviate months
        },
      },
      yaxis: {
        labels: {
          align: "left",
          minWidth: 0,
          maxWidth: 140,
          style: {
            colors: "#9ca3af",
            fontSize: "13px",
            fontFamily: "Inter, ui-sans-serif",
            fontWeight: 400,
          },
          formatter: (value) => (value >= 1000 ? `${value / 1000}k` : value), // Format Y axis labels
        },
      },
      states: {
        hover: {
          filter: {
            type: "darken",
            value: 0.9,
          },
        },
      },
      tooltip: {
        y: {
          formatter: (value) =>
            `$${value >= 1000 ? `${value / 1000}k` : value}`, // Tooltip formatter
        },
        custom: function (props) {
          const { categories } = props.ctx.opts.xaxis;
          const { dataPointIndex } = props;
          const title = categories[dataPointIndex];
          const newTitle = `${title}`;

          return `<div class="tooltip"><strong>${newTitle}</strong><br>$${props.series[0][dataPointIndex]}</div>`;
        },
      },
      responsive: [
        {
          breakpoint: 568,
          options: {
            chart: {
              height: "100%", // Agar chart responsif
            },
            plotOptions: {
              bar: {
                columnWidth: "14px",
              },
            },
            stroke: {
              width: 8,
            },
            labels: {
              style: {
                colors: "#9ca3af",
                fontSize: "11px",
                fontFamily: "Inter, ui-sans-serif",
                fontWeight: 400,
              },
              offsetX: -2,
              formatter: (title) => title.slice(0, 3), // Abbreviate months on small screens
            },
            yaxis: {
              labels: {
                align: "left",
                minWidth: 0,
                maxWidth: 140,
                style: {
                  colors: "#9ca3af",
                  fontSize: "11px",
                  fontFamily: "Inter, ui-sans-serif",
                  fontWeight: 400,
                },
                formatter: (value) =>
                  value >= 1000 ? `${value / 1000}k` : value, // Format Y axis labels
              },
            },
          },
        },
      ],
    };

    var chart = new ApexCharts(
      document.querySelector("#hs-single-bar-chart"),
      options
    );
    chart.render();
  })();
});
