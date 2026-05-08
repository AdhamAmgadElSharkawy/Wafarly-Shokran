from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from transactions.models import Transaction
from django.db.models.functions import TruncMonth,TruncDate
from django.db.models import Sum,Q,Count
from django.utils import timezone
import datetime

# Create your views here.
@login_required(login_url='login')
def reports(request):
    """
    Renders the financial reports and analytics page for the authenticated user.

    This view handles the aggregation and filtering of transaction data based on 
    a specified time period (this_month, last_month, this_year, last_year, or all).
    
    It performs several database-level aggregations:
    - Calculates total income, total expenses, and the net balance.
    - Computes the average monthly savings based on the distinct months available.
    - Aggregates daily income and expense trends for chronological charts.
    - Groups expense transactions by category and date to show spending patterns.

    Args:
        request: The HTTP request object, which may contain a 'period' GET parameter.

    Returns:
        HttpResponse: Renders the 'reports.html' template with the aggregated financial data in the context.
    """
    today = timezone.now().date()
    period=request.GET.get('period','all')
    transactions_data = Transaction.objects.filter(user=request.user)

    if period == 'this_month':
        transactions_data=transactions_data.filter(date_time__year=today.year, date_time__month=today.month)
    
    elif period == 'last_month':
        last_month = today.replace(day=1) - datetime.timedelta(days=1)
        transactions_data=transactions_data.filter(date_time__year=last_month.year, date_time__month=last_month.month)
    
    elif period == 'this_year':
        transactions_data=transactions_data.filter(date_time__year=today.year)
    
    elif period == 'last_year':
        last_year=today.year - 1
        transactions_data=transactions_data.filter(date_time__year=last_year)


    stats=transactions_data.annotate(
        month=TruncMonth('date_time')
    ).aggregate(
        total_income=Sum('amount', filter=Q(type='i')),
        total_expense=Sum('amount', filter=Q(type='e')),
        months_count=Count('month', distinct=True) 
    )

    total_income = float(stats['total_income'] or 0)
    total_expense = float(stats['total_expense'] or 0)
    months_count = stats['months_count'] or 0

    if months_count > 0:
        monthly_avg = (total_income - total_expense) / months_count
    else:
        monthly_avg = 0


    daily_data = transactions_data.annotate(
        date=TruncDate('date_time')
    ).values('date').annotate(
        total_income=Sum('amount', filter=Q(type='i')),
        total_expense=Sum('amount', filter=Q(type='e')),
    ).order_by('date')


    transactions_per_category = transactions_data.filter(type='e').annotate(
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
        'transPerCategory':list(transactions_per_category),
    }

    return render(request,'reports.html',context)