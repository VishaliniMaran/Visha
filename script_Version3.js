// Minimal dashboard script (sample data baked in)
const data = {
  servicesSummary: [
    { category: 'Project Coordination', numServices: 23, tickets: 313, totalEngSavingHrs: 3003.5, totalEngSavingWks: 79 },
    { category: 'Testing', numServices: 4, tickets: 40, totalEngSavingHrs: 914, totalEngSavingWks: 24 },
    { category: 'Documentation', numServices: 13, tickets: 596, totalEngSavingHrs: 4643, totalEngSavingWks: 122 }
  ],
  totals: { numServices: 40, tickets: 949, totalEngSavingHrs: 8561, totalEngSavingWks: 225 }
};

function formatNumber(v){
  if (Number.isInteger(v)) return v.toString();
  return v.toLocaleString(undefined, { maximumFractionDigits: 1 });
}

function init(){
  document.getElementById('kpiTickets').textContent = formatNumber(data.totals.tickets);
  document.getElementById('kpiHours').textContent = formatNumber(data.totals.totalEngSavingHrs);
  document.getElementById('kpiWeeks').textContent = formatNumber(data.totals.totalEngSavingWks);

  const colors = ['#2f7ef7','#28c76f','#ff9800'];

  // Tickets doughnut
  const tCtx = document.getElementById('ticketsChart').getContext('2d');
  new Chart(tCtx, {
    type: 'doughnut',
    data: { labels: data.servicesSummary.map(s => s.category), datasets: [{ data: data.servicesSummary.map(s => s.tickets), backgroundColor: colors }] },
    options: { plugins: { legend: { display: true, labels: { color: '#9aa3ad' } } } }
  });

  // Saving hours bar
  const hCtx = document.getElementById('hoursChart').getContext('2d');
  new Chart(hCtx, {
    type: 'bar',
    data: { labels: data.servicesSummary.map(s => s.category), datasets: [{ data: data.servicesSummary.map(s => s.totalEngSavingHrs), backgroundColor: colors }] },
    options: { scales: { y: { ticks: { color: '#9aa3ad' }, beginAtZero: true }, x: { ticks: { color: '#9aa3ad' } } }, plugins: { legend: { display: false } } }
  });

  // Weeks horizontal bar
  const wCtx = document.getElementById('weeksChart').getContext('2d');
  new Chart(wCtx, {
    type: 'bar',
    data: { labels: data.servicesSummary.map(s => s.category), datasets: [{ data: data.servicesSummary.map(s => s.totalEngSavingWks), backgroundColor: colors }] },
    options: { indexAxis: 'y', scales: { x: { ticks: { color: '#9aa3ad' }, beginAtZero: true }, y: { ticks: { color: '#9aa3ad' } } }, plugins: { legend: { display: false } } }
  });

  document.getElementById('exportPdfBtn').addEventListener('click', exportPdf);
}

async function exportPdf(){
  const container = document.querySelector('.wrap');
  const canvas = await html2canvas(container, { scale: 2 });
  const img = canvas.toDataURL('image/jpeg', 0.95);
  const { jsPDF } = window.jspdf;
  const pdf = new jsPDF('p','mm','a4');
  const pageWidth = pdf.internal.pageSize.getWidth();
  const imgProps = pdf.getImageProperties(img);
  const imgWidth = pageWidth - 16;
  const imgHeight = (imgProps.height * imgWidth) / imgProps.width;
  pdf.addImage(img, 'JPEG', 8, 8, imgWidth, imgHeight);
  pdf.save('RnD_Services_Dashboard.pdf');
}

window.addEventListener('DOMContentLoaded', init);