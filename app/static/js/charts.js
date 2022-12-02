function CateStats(labels, data) {
    const ctx = document.getElementById('cateStats');
    new Chart (ctx, {
        type: 'pie',
        data: {
            labels: labels,
            datasets: [{
                label: 'Số lượng',
                data: data,
                borderWidth: 1
            }]

        },
        option: {
            scale: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}
function RevenueStats(labels, data) {
    const ctx = document.getElementById('revenueStats');
    const rndNum = () => Math.floor(Math.random() * (255 - 50 + 1) + 50);
    const rndRGBA = () => `rgba(${rndNum()}, ${rndNum()}, ${rndNum()}, 0.7)`;
    new Chart (ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Doanh thu',
                data: data,
                borderWidth: 1
                backgroundColor: ['red', 'blue', 'green', 'rndRGBA()', 'rndRGBA()']
            }]
        },
        option: {
            scale: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}