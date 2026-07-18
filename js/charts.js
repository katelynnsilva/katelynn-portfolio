const NAVY = "#1f3864";
const NAVY_LIGHT = "#5b8def";
const GRAY = "#a0a8b8";

fetch("charts/data.json")
  .then((res) => res.json())
  .then((data) => {
    renderMonthly(data.monthly_revenue);
    renderChannel(data.by_channel);
    renderLocation(data.by_location);
    renderCategory(data.by_category);
  })
  .catch((err) => console.error("Failed to load chart data:", err));

function renderMonthly(rows) {
  new Chart(document.getElementById("chart-monthly"), {
    type: "line",
    data: {
      labels: rows.map((r) => r.month),
      datasets: [{
        label: "Monthly Revenue ($)",
        data: rows.map((r) => r.revenue),
        borderColor: NAVY,
        backgroundColor: "rgba(31,56,100,0.1)",
        fill: true,
        tension: 0.3,
      }],
    },
    options: { responsive: true, maintainAspectRatio: false, plugins: { title: { display: true, text: "Monthly Revenue Trend" } } },
  });
}

function renderChannel(rows) {
  new Chart(document.getElementById("chart-channel"), {
    type: "bar",
    data: {
      labels: rows.map((r) => r.channel),
      datasets: [{
        label: "Margin %",
        data: rows.map((r) => r.margin_pct),
        backgroundColor: [NAVY, NAVY_LIGHT],
      }],
    },
    options: { responsive: true, maintainAspectRatio: false, plugins: { title: { display: true, text: "Profit Margin: In-Store vs Online" } } },
  });
}

function renderLocation(rows) {
  new Chart(document.getElementById("chart-location"), {
    type: "bar",
    data: {
      labels: rows.map((r) => r.location),
      datasets: [{
        label: "Profit ($)",
        data: rows.map((r) => r.profit),
        backgroundColor: rows.map((r) => (r.profit < 0 ? "#c0392b" : NAVY)),
      }],
    },
    options: {
      indexAxis: "y",
      responsive: true,
      maintainAspectRatio: false,
      plugins: { title: { display: true, text: "Profit by Location" } },
    },
  });
}

function renderCategory(rows) {
  new Chart(document.getElementById("chart-category"), {
    type: "bar",
    data: {
      labels: rows.map((r) => r.category),
      datasets: [{
        label: "Margin %",
        data: rows.map((r) => r.margin_pct),
        backgroundColor: rows.map((r) => (r.margin_pct < 0 ? "#c0392b" : NAVY_LIGHT)),
      }],
    },
    options: { responsive: true, maintainAspectRatio: false, plugins: { title: { display: true, text: "Profit Margin by Category" } } },
  });
}
