document.addEventListener("DOMContentLoaded", function () {
  const form = document.getElementById("stock-form");
  const chartCanvas = document.getElementById("priceChart");
  const portfolioDiv = document.getElementById("portfolio-info");
  let chartInstance;

  form.addEventListener("submit", async function (e) {
    e.preventDefault();
    const symbol = document.getElementById("symbol").value;
    const strategy = document.getElementById("strategy").value;

    const formData = new FormData();
    formData.append("symbol", symbol);
    formData.append("strategy", strategy);

    const res = await fetch("/stock", {
      method: "POST",
      body: formData,
    });

    const data = await res.json();
    if (data.error) return alert(data.error);

    const labels = Object.keys(data.prices);
    const values = Object.values(data.prices);

    if (chartInstance) chartInstance.destroy();
    chartInstance = new Chart(chartCanvas, {
      type: "line",
      data: {
        labels: labels,
        datasets: [{
          label: symbol + " Closing Price",
          data: values,
          borderColor: "blue",
          borderWidth: 2,
          pointBackgroundColor: labels.map(d => {
            const s = data.signals[d];
            if (s === "BUY") return "green";
            if (s === "SELL") return "red";
            return "blue";
          }),
          pointRadius: 5
        }]
      },
      options: {
        responsive: true
      }
    });

    portfolioDiv.innerHTML = `
      <p>💰 Cash: ₹${data.portfolio.cash}</p>
      <p>📈 Total Value: ₹${data.portfolio.total_value}</p>
      <p>📦 Holdings: ${JSON.stringify(data.portfolio.holdings)}</p>
    `;
  });
});
