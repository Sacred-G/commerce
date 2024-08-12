// Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily = '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#292b2c';

// Area Chart Example
var ctxLine = document.getElementById('myAreaChart').getContext('2d');
var auctionActivityChart = new Chart(ctxLine, {
    type: 'line',
    data: {
        labels: ['Day 1', 'Day 2', 'Day 3', 'Day 4', 'Day 5', 'Day 6', 'Day 7'],
        datasets: [{
            label: 'New Listings',
            data: [12, 19, 3, 5, 2, 3, 10],
            borderColor: 'rgb(75, 192, 192)',
            tension: 0.1
        }, {
            label: 'Bids Placed',
            data: [7, 11, 5, 8, 3, 7, 15],
            borderColor: 'rgb(255, 99, 132)',
            tension: 0.1
        }]
    },
    options: {
        responsive: true,
        plugins: {
            legend: {
                position: 'top',
            },
            title: {
                display: true,
                text: 'Recent Auction Activity'
            }
        },
        scales: {
            y: {
                beginAtZero: true
            }
        }
    }
});
