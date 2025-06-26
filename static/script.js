let chart;

async function fetchData(symbol) {
  const response = await fetch(`/compare?symbol=${symbol}`);
  return await response.json();
}

function renderChart(dates, strategy, stock, label) {
  const ctx = document.getElementById("strategyChart").getContext("2d");
  if (chart) chart.destroy();

  chart = new Chart(ctx, {
    type: "line",
    data: {
      labels: dates,
      datasets: [
        {
          label: "Your Strategy",
          data: strategy,
          borderColor: "#2e86de",
          fill: false,
          tension: 0.3
        },
        {
          label: label,
          data: stock,
          borderColor: "#e74c3c",
          fill: false,
          tension: 0.3
        }
      ]
    },
    options: {
      responsive: true,
      scales: {
        x: { ticks: { maxTicksLimit: 10 } },
        y: { beginAtZero: false }
      }
    }
  });
}

async function updateChart() {
  const symbol = document.getElementById("stockSelect").value;
  const data = await fetchData(symbol);
  renderChart(data.dates, data.strategy, data.stock, symbol);
}

// Auto-load default
updateChart();
