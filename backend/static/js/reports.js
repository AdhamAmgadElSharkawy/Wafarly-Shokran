const ctx1 = document.getElementById('incomeExpenseChart').getContext('2d');
const ctx2 = document.getElementById('categorySpendingChart').getContext('2d');
const totalIncome = JSON.parse(document.getElementById('income-data').textContent);
const totalExpense = JSON.parse(document.getElementById('expense-data').textContent);
const monthlyData = JSON.parse(document.getElementById('monthly-chart-data').textContent);

const chartLabels = [];
const incomeData = [];
const expenseData = [];
const savingData = [];

monthlyData.forEach( item => {
    const dateObj = new Date(item.month);
    chartLabels.push(dateObj.toLocaleString('en-US', { month: 'short', year: 'numeric' }));
    incomeData.push(item.total_income || 0);
    expenseData.push( item.total_expense || 0 );
    savingData.push((item.totalIncome || 0) - (item.total_expense || 0));
} );

const incomeExpenseChart = new Chart(ctx1, {
    type: 'line', 
    
    data: {
        labels: chartLabels,
        datasets: [
            {
                label: 'Income',
                data: incomeData, 
                borderColor: '#00b862', 
                backgroundColor: '#00b862', 
                tension: 0.4, 
                fill: false
            },
            {
                label: 'Expenses',
                data: expenseData,
                borderColor: '#ff4d4d', 
                backgroundColor: '#ff4d4d',
                tension: 0.4,
                fill: false
            },
            {
                label: 'Savings',
                data: savingData,
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


function IncomeExpenseChartSheet() {
    const labels = incomeExpenseChart.data.labels;
    const datasets = incomeExpenseChart.data.datasets;
    
    const excelData = [];
    
    const headers = [''];
    datasets.forEach(ds => headers.push(ds.label || 'Amount'));
    excelData.push( headers ); 

    for (let i = 0; i < labels.length; i++) {
        const row = [labels[i]];
        datasets.forEach(ds => {
            row.push(ds.data[i]);
        });
        excelData.push(row);
    }

    return XLSX.utils.aoa_to_sheet(excelData);
}


const rawData = JSON.parse( document.getElementById( 'transactionsPerCategory' ).textContent );
const months = [...new Set(rawData.map(item => item.month))];
const categories = [...new Set(rawData.map(item => item.category__name))];

const formattedMonths = months.map(dateString => {
    const dateObj = new Date(dateString);
    return dateObj.toLocaleDateString('en-US', {month: 'short', year: 'numeric'});
});

const dataLookup = {};

rawData.forEach( item => {
    if (!dataLookup[item.category__name]) {
        dataLookup[item.category__name] = {};
    }
    dataLookup[item.category__name][item.month] = item.total_amount;
});

const chartDatasets = categories.map(category => {
    return {
        label: category,
        data: months.map( month => {
            const dateObj = new Date(month);
            return dataLookup[category][month] || 0; 
        }),
        borderWidth: 2,
    };
});

const categorySpendingChart = new Chart( ctx2, {
    type: 'bar',
    data:{
        labels: formattedMonths,
        datasets:chartDatasets
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


function categoryChartSheet() {
    const labels = categorySpendingChart.data.labels;
    const datasets = categorySpendingChart.data.datasets;
    
    const excelData = [];
    
    const headers = ['Category'];
    datasets.forEach(ds => headers.push(ds.label || 'Amount'));
    excelData.push( headers ); 

    for (let i = 0; i < labels.length; i++) {
        const row = [labels[i]];
        datasets.forEach(ds => {
            row.push(ds.data[i]);
        });
        excelData.push(row);
    }

    return XLSX.utils.aoa_to_sheet(excelData);
}

function exportChartsToExcel() {
    const IncomeExpenseSheet = IncomeExpenseChartSheet();
    const CategorySpendingSheet = categoryChartSheet();

    const workbook = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(workbook, IncomeExpenseSheet, "Income vs Expenses Trend");
    XLSX.utils.book_append_sheet(workbook, CategorySpendingSheet, "Category Spending");
    XLSX.writeFile(workbook, "Charts_Data.xlsx");
}
