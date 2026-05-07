from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from transactions.models import Transaction
from django.db.models.functions import TruncMonth,TruncDay,TruncDate
from django.db.models import Sum,Q,Count

# Create your views here.
@login_required(login_url='login')
def reports(request):

    transactions_data = Transaction.objects.filter(user=request.user).annotate(
        month=TruncMonth('date_time')
    ).aggregate(
        total_income=Sum('amount', filter=Q(type='i')),
        total_expense=Sum('amount', filter=Q(type='e')),
        months_count=Count('month', distinct=True) 
    )

    total_income = float(transactions_data['total_income'] or 0)
    total_expense = float(transactions_data['total_expense'] or 0)
    months_count = transactions_data['months_count'] or 0

    if months_count > 0:
        monthly_avg = (total_income - total_expense) / months_count
    else:
        monthly_avg = 0

    daily_data = Transaction.objects.filter(user=request.user).annotate(
        date=TruncDate('date_time')
    ).values('date').annotate(
        total_income=Sum('amount', filter=Q(type='i')),
        total_expense=Sum('amount', filter=Q(type='e')),
    ).order_by('date')

    transactionsPerCategory= Transaction.objects.filter(type='e',user=request.user).annotate(
    date=TruncDate('date_time')
).values('category__name', 'date').annotate(
    total_amount=Sum('amount')
).order_by('date')


    context = {
        'ti':total_income,
        'te':total_expense,
        'ts':total_income-total_expense,
        'dailyData':list(daily_data),
        'monthlyAvg':monthly_avg,
        'transPerCategory':list(transactionsPerCategory),
    }

    return render(request,'reports.html',context)