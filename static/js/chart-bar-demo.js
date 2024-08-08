Chart.defaults.global.defaultFontFamily = '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#292b2c';

// Fetch category data and create bar chart
fetch('/category-data/')
    .then(response => response.json())
    .then(data => {
        const ctxBarChart = document.getElementById('myBarChart');
        const myBarChart = new Chart(ctxBarChart, {
            type: 'bar',
            data: {
                labels: data.map(item => item.name),
                datasets: [{
                    label: 'Number of Listings',
                    backgroundColor: 'rgba(2,117,216,0.8)',
                    borderColor: 'rgba(2,117,216,1)',
                    data: data.map(item => item.count),
                }],
            },
            options: {
                scales: {
                    xAxes: [{
                        gridLines: {
                            display: false
                        },
                        ticks: {
                            maxTicksLimit: 10
                        }
                    }],
                    yAxes: [{
                        ticks: {
                            min: 0,
                            max: Math.max(...data.map(item => item.count)) + 1,
                            maxTicksLimit: 5
                        },
                        gridLines: {
                            display: true
                        }
                    }],
                },
                legend: {
                    display: false
                },
                title: {
                    display: true,
                    text: 'Number of Listings per Category'
                }
            }
        });
    })
    .catch(error => console.error('Error:', error));
