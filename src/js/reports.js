const ctx1 = document.getElementById('incomeExpenseChart').getContext('2d');
const ctx2 = document.getElementById('categorySpendingChart').getContext('2d');

const incomeExpenseChart = new Chart(ctx1, {
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
} );

const categorySpendingChart = new Chart( ctx2, {
    type: 'bar',
    data:{
        labels: ['Oct', 'Nov', 'Dec', 'Jan', 'Feb', 'Mar'],
        datasets:[
            {
                label: 'Housing',
                data: [1200, 1200, 1200, 1200, 1200, 1200],
                backgroundColor: '#3b82f6',
            },
            {
                label: 'Food',
                data: [650, 720, 580, 670, 630, 680],
                backgroundColor: '#F59E0B',
            },
            {
                label: 'Transportation',
                data: [420, 480, 390, 460, 440,450],
                backgroundColor: '#10B981',
            },
            {
                label: 'Entertainment',
                data: [280, 350, 230, 310, 280, 320],
                backgroundColor: '#8B5CF6',
            },
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
                x: {
                    stacked: true,
                },
                y: {
                    stacked: true
                }
            }
    }
} );
