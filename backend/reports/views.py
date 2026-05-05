from django.shortcuts import render
from transactions.models import Transaction, Category

# Create your views here.
def reports(request):
    transactionsData=Transaction.objects.all()
    
    total_income = 0
    total_expense = 0
    for i in transactionsData.filter(type='i'):
        total_income+=i.amount
    for e in transactionsData.filter(type='e'):
        total_expense+=e.amount
    
    context = {
        'ti':total_income,
        'te':total_expense,
        'ts':total_income-total_expense,
    }
    return render(request,'reports.html',context)