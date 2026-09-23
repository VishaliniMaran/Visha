const services = [
  { category: "Project Coordination", tickets: 313, hours: 3003.5, weeks: 79 },
  { category: "Testing", tickets: 40, hours: 914, weeks: 24 },
  { category: "Documentation", tickets: 596, hours: 4643, weeks: 122 }
];

const colors = ["#356ae6", "#18a66a", "#f28a35"];
const number = (value, digits = 0) => value.toLocaleString(undefined, { maximumFractionDigits: digits });

function chartOptions(extra = {}) {
  return {
    responsive: true,
    maintainAspectRatio: false,
    plugins: { legend: { labels: { color: "#526174", usePointStyle: true, padding: 18 } } },
    scales: {
      x: { grid: { display: false }, ticks: { color: "#718096" } },
      y: { beginAtZero: true, border: { display: false }, grid: { color: "#edf0f5" }, ticks: { color: "#718096" } }
    },
    ...extra
  };
}

function renderDashboard() {
  const totals = services.reduce((result, service) => ({
    tickets: result.tickets + service.tickets,
    hours: result.hours + service.hours,
    weeks: result.weeks + service.weeks
  }), { tickets: 0, hours: 0, weeks: 0 });

  document.getElementById("kpiTickets").textContent = number(totals.tickets);
  document.getElementById("kpiHours").textContent = number(totals.hours, 1);
  document.getElementById("kpiWeeks").textContent = number(totals.weeks);
  document.getElementById("metricsTable").innerHTML = services.map(service => `
    <tr><td><strong>${service.category}</strong></td><td>${number(service.tickets)}</td><td>${number(service.hours, 1)}</td><td>${number(service.weeks)}</td></tr>`).join("");

  new Chart(document.getElementById("ticketsChart"), {
    type: "doughnut",
    data: { labels: services.map(s => s.category), datasets: [{ data: services.map(s => s.tickets), backgroundColor: colors, borderWidth: 3, borderColor: "#fff" }] },
    options: { responsive: true, maintainAspectRatio: false, cutout: "64%", plugins: { legend: { position: "bottom", labels: { color: "#526174", usePointStyle: true, padding: 18 } } } }
  });

  new Chart(document.getElementById("hoursChart"), {
    type: "bar",
    data: { labels: services.map(s => s.category), datasets: [{ label: "Saving Hours", data: services.map(s => s.hours), backgroundColor: colors, borderRadius: 6, barPercentage: .62 }] },
    options: chartOptions({ plugins: { legend: { display: false }, tooltip: { callbacks: { label: item => ` ${number(item.raw, 1)} hours` } } } })
  });

  new Chart(document.getElementById("weeksChart"), {
    type: "bar",
    data: { labels: services.map(s => s.category), datasets: [{ label: "Savings (Week)", data: services.map(s => s.weeks), backgroundColor: colors, borderRadius: 6, barPercentage: .58 }] },
    options: chartOptions({ indexAxis: "y", plugins: { legend: { display: false } }, scales: { x: { beginAtZero: true, grid: { color: "#edf0f5" }, ticks: { color: "#718096" } }, y: { grid: { display: false }, ticks: { color: "#718096" } } } })
  });
}

document.addEventListener("DOMContentLoaded", renderDashboard);
document.getElementById("exportBtn").addEventListener("click", async () => {
  const canvas = await html2canvas(document.getElementById("dashboardRoot"), { backgroundColor: "#f5f7fb", scale: 2 });
  const link = document.createElement("a");
  link.download = "rnd-services-metrics.png";
  link.href = canvas.toDataURL("image/png");
  link.click();
});
