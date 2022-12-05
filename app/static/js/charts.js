function drawCateStats (labels, data) {
    const ctx = document.getElementById('cateStats');

  new Chart(ctx, {
    type: 'pie',
    data: {
      labels: labels,
      datasets: [{
        label: 'Số Lượng',
        data: data,
        borderWidth: 1
      }]
    },
    options: {
      scales: {
        y: {
          beginAtZero: true
        }
      }
    }
  });
}

function drawRevenueStats (labels, data) {
    const ctx = document.getElementById('revenueStats');
//    const rndNum = () => Math.floor(Math.random() * (255 - 55 + 1) + 55);
//    const rndRGBA = () => `rgba(${rndNum()}, ${rndNum()}, ${rndNum()}, 1)`;
  new Chart(ctx, {
    type: 'bar',
    data: {
      labels: labels,
      datasets: [{
        label: 'Doanh Thu',
        data: data,
        borderWidth: 1,
 backgroundColor: ['red', 'blue', 'green', 'rgba(100, 200, 150, 0.8)']
      }]
    },
    options: {
      scales: {
        y: {
          beginAtZero: true
        }
      }
    }
  });
}