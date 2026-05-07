document.addEventListener("DOMContentLoaded",function(){
    const categoryNames = JSON.parse(document.getElementById('spending_category_name_data').textContent) ;
    const categoryTotals = JSON.parse(document.getElementById('spending_category_total_data').textContent) ;
    const totalIncome= JSON.parse(document.getElementById('total_income_data').textContent) ;
    const totalExpenses = JSON.parse(document.getElementById('total_expenses_data').textContent) ;

    const pieChart = document.getElementById('piechart').getContext('2d');
    new Chart(pieChart,{
        type:'doughnut',
        data: {
            labels : categoryNames,
            datasets: [{
                data: categoryTotals,
                backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF', '#FF9F40'],
                borderWidth: 0
            }]
        },
        options:{
            responsive:true,
            maintainAspectRatio:false
        }


    });
    const barchart = document.getElementById('barChart').getContext('2d');
    new Chart(barchart,{
        type:'bar',
        data: {
            labels : ['Total Income','Total Expenses'],
            datasets: [{
                label:'Amount',
                data: [totalIncome,totalExpenses],
                backgroundColor: ['#FF6384', '#4BC0C0'],
                borderRadius:8
            }]
        },
        options:{
            responsive:true,
            maintainAspectRatio:false,
            scales:{y:{beginAtZero:true}},
            plugins:{legend:{display:false}}
        }


    });

});
