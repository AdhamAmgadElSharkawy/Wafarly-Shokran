from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from transactions.models import Transaction
from django.db.models.functions import TruncMonth
from django.db.models import Sum,Q

# Create your views here.
@login_required(login_url='login')
def reports(request):
    transactionsData=Transaction.objects.filter(user=request.user)

    total_income = 0
    total_expense = 0
    
    for i in transactionsData.filter(type='i'):
        total_income+=i.amount
    for e in transactionsData.filter(type='e'):
        total_expense+=e.amount
    
    monthlyData = Transaction.objects.filter(user=request.user).annotate(
        month=TruncMonth('date_time')
    ).values('month').annotate(
        total_income=Sum('amount', filter=Q(type='i')),
        total_expense=Sum('amount', filter=Q(type='e')),
    ).order_by('month')

    transactionsPerCategory= Transaction.objects.filter(type='e',user=request.user).annotate(
    month=TruncMonth('date_time')
).values('category__name', 'month').annotate(
    total_amount=Sum('amount')
).order_by('month')

    monthlyAvg=0
    n=0
    for d in monthlyData:
        income = d['total_income'] or 0
        expense = d['total_expense'] or 0
        monthlyAvg+= income - expense
        n+=1
    
    if n > 0:
        monthlyAvg = monthlyAvg / n
    else:
        monthlyAvg = 0

    context = {
        'ti':total_income,
        'te':total_expense,
        'ts':total_income-total_expense,
        'monthlyAvg':monthlyAvg,
        'monthlyData':list(monthlyData),
        'transPerCategory':list(transactionsPerCategory),
    }
    return render(request,'reports.html',context)