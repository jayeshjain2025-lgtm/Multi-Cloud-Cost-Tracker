let serviceChart, dailyChart;

function drawCharts(json) {
  const { services, service_costs, dates, daily_totals, total } = json;
  document.getElementById('total').innerText = `$${total.toFixed(2)}`;

  if (serviceChart) serviceChart.destroy();
  serviceChart = new Chart(
    document.getElementById('serviceChart'),
    { type: 'bar',
      data: { labels: services, datasets: [{ data: service_costs }] },
      options: { plugins: { legend: { display: false } } }
    });

  if (dailyChart) dailyChart.destroy();
  dailyChart = new Chart(
    document.getElementById('dailyChart'),
    { type: 'line',
      data: { labels: dates, datasets: [{ data: daily_totals, borderColor: 'rgb(50,150,255)', fill: false }] },
      options: { plugins: { legend: { display: false } } }
    });
}

async function loadData() {
  try {
    const res = await fetch(endpoint);
    const json = await res.json();
    drawCharts(json);
  } catch (e) {
    console.error(e);
    document.getElementById('total').innerText = 'Error';
  }
}

window.addEventListener('DOMContentLoaded', loadData);
