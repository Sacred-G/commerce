Chart.defaults.global.defaultFontFamily = '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#292b2c';

// Pie Chart Example
const ctxPieChart = document.getElementById("myPieChart");

fetch('/category-data/')  // Adjust this URL if necessary
    .then(response => response.json())
    .then(data => {
        const myPieChart = new Chart(ctxPieChart, {
            type: 'pie',
            data: {
                labels: data.map(item => item.name),
                datasets: [{
                    data: data.map(item => item.count),
                    backgroundColor: [
                        '#007bff', '#dc3545', '#ffc107', '#28a745',
                        '#17a2b8', '#6c757d', '#343a40', '#f8f9fa',
                        '#20c997', '#e83e8c', '#6610f2', '#fd7e14'
                    ],
                }],
            },
        });
    })
    .catch(error => console.error('Error:', error));