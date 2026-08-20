// script.js - CMY R&D dashboard (sample data baked in)
// Creates charts and supports browser PDF export via html2canvas + jsPDF

const sampleData = {
  servicesSummary: [
    { category: 'Project Coordination', numServices: 23, tickets: 313, totalEngSavingHrs: 3003.5, totalEngSavingWks: 79 },
    { category: 'Testing', numServices: 4, tickets: 40, totalEngSavingHrs: 914, totalEngSavingWks: 24 },
    { category: 'Documentation', numServices: 13, tickets: 596, totalEngSavingHrs: 4643, totalEngSavingWks: 122 }
  ],
  totals: { numServices: 40, tickets: 949, totalEngSavingHrs: 8561, totalEngSavingWks: 225 }
};

function renderSummary(summary){
  document.getElementById('totalServices').textContent = summary.totals.numServices;
  document.getElementById('totalTickets').textContent = summary.totals.tickets;
  document.getElementById('totalHrs').textContent = summary.totals.totalEngSavingHrs;
  document.getElementById('totalWks').textContent = summary.totals.totalEngSavingWks;

  const container = document.getElementById('servicesList');
  container.innerHTML = '';
  summary.servicesSummary.forEach(s => {
    const el = document.createElement('div');
    el.className = 'service-item';
    el.innerHTML = `\n      <h4>${s.category}</h4>\n      <p><strong># Services:</strong> ${s.numServices}</p>\n      <p><strong># Tickets:</strong> ${s.tickets}</p>\n      <p><strong>Total Eng Saving (Hrs):</strong> ${s.totalEngSavingHrs}</p>\n      <p><strong>Total Eng Saving (Wks):</strong> ${s.totalEngSavingWks}</p>\n    `;
    container.appendChild(el);
  });
}

let ticketsChart, savingHoursChart, weeklyChart;

function createTicketsChart(ctx, data){
  const labels = data.map(d => d.category);
  const values = data.map(d => d.tickets);
  return new Chart(ctx, { type: 'doughnut', data: { labels, datasets: [{ data: values, backgroundColor: ['#60a5fa','#34d399','#f97316'] }] }, options: { plugins: { legend: { position: 'bottom' } } } });
}

function createSavingHoursChart(ctx, data){
  const labels = data.map(d => d.category);
  const values = data.map(d => d.totalEngSavingHrs);
  return new Chart(ctx, { type: 'bar', data: { labels, datasets: [{ label: 'Saved hours', data: values, backgroundColor: '#7c3aed' }] }, options: { scales: { y: { beginAtZero: true, title: { display: true, text: 'Hours' } } }, plugins: { legend: { display: false } } } });
}

function generateWeeklyTrend(totalHours){
  // create a synthetic 8-week trend that sums approximately to totalHours
  const weeks = 8;
  const labels = [];
  const values = [];
  const now = new Date();
  const base = Math.floor(totalHours / (weeks * 1.2));
  for(let i = weeks - 1; i >= 0; i--){
    const d = new Date(now);
    d.setDate(now.getDate() - i * 7);
    const label = d.toISOString().slice(0,10);
    labels.push(label);
  }
  // simple increasing pattern
  let remaining = totalHours;
  for(let i=0;i<weeks;i++){
    const factor = 0.8 + (i / (weeks - 1)) * 0.8; // from 0.8 to 1.6
    const val = Math.round((totalHours / weeks) * factor);
    values.push(val);
    remaining -= val;
  }
  // adjust last value to match totalHours
  values[values.length - 1] += Math.round(remaining);
  return { labels, values };
}

function createWeeklyChart(ctx, labels, values){
  return new Chart(ctx, { type: 'line', data: { labels, datasets: [{ label: 'Weekly saved hours', data: values, borderColor: '#0ea5e9', backgroundColor: 'rgba(14,165,233,0.12)', fill: true, tension: 0.2, pointRadius: 4 }] }, options: { scales: { y: { beginAtZero: true, title: { display: true, text: 'Hours' } } }, plugins: { legend: { display: false } } } });
}

function initDashboard(data){
  renderSummary(data);
  const ticketsCtx = document.getElementById('ticketsChart').getContext('2d');
  const hoursCtx = document.getElementById('savingHoursChart').getContext('2d');
  const weeklyCtx = document.getElementById('weeklySavingsChart').getContext('2d');

  if(ticketsChart) ticketsChart.destroy();
  if(savingHoursChart) savingHoursChart.destroy();
  if(weeklyChart) weeklyChart.destroy();

  ticketsChart = createTicketsChart(ticketsCtx, data.servicesSummary);
  savingHoursChart = createSavingHoursChart(hoursCtx, data.servicesSummary);
  const weekly = generateWeeklyTrend(data.totals.totalEngSavingHrs);
  weeklyChart = createWeeklyChart(weeklyCtx, weekly.labels, weekly.values);
}

async function exportPdfBrowser(){
  const container = document.querySelector('.container');
  const canvas = await html2canvas(container, { scale: 2 });
  const imgData = canvas.toDataURL('image/jpeg', 0.95);
  const { jsPDF } = window.jspdf;
  const pdf = new jsPDF('p', 'mm', 'a4');
  const pageWidth = pdf.internal.pageSize.getWidth();
  const imgProps = pdf.getImageProperties(imgData);
  const imgWidth = pageWidth - 10;
  const imgHeight = (imgProps.height * imgWidth) / imgProps.width;
  pdf.addImage(imgData, 'JPEG', 5, 10, imgWidth, imgHeight);
  pdf.save('cmy-rd-dashboard.pdf');
}

document.addEventListener('DOMContentLoaded', () => {
  initDashboard(sampleData);
  document.getElementById('exportPdfBtn').addEventListener('click', exportPdfBrowser);
});
