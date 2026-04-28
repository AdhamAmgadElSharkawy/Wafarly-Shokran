const ctx = document.getElementById('incomeExpenseChart').getContext('2d');

const myChart = new Chart(ctx, {
    type: 'line', 
    data: {
        labels: ['Jul 25', 'Aug 25', 'Sep 25', 'Oct 25', 'Nov 25', 'Dec 25'],
        datasets: [
            {
                label: 'Income',
                data: [4200, 4500, 4100, 4500, 4500, 5200], 
                borderColor: '#00b862', 
                backgroundColor: '#00b862', 
                tension: 0.4, 
                fill: false
            },
            {
                label: 'Expenses',
                data: [3100, 3300, 2900, 2800, 3200, 2500],
                borderColor: '#ff4d4d', 
                backgroundColor: '#ff4d4d',
                tension: 0.4,
                fill: false
            },
            {
                label: 'Savings',
                data: [1100, 1200, 1300, 1700, 1300, 2500],
                borderColor: '#3b82f6', 
                backgroundColor: '#3b82f6',
                tension: 0.4,
                fill: false
            }
        ]
    },
    options: {
        responsive: true,
        plugins: {
            legend: {
                position: 'bottom', 
            }
        },
        scales: {
            y: {
                beginAtZero: true 
            }
        }
    }
});