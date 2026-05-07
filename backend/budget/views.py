from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Budget
from transactions.models import Category

@login_required
def budget_create(request):
    categories = Category.objects.all()
    
    if request.method == 'POST':
        category_id = request.POST.get('category')
        limit = request.POST.get('amount')
        end_date = request.POST.get('period')
        over_limit_alert = request.POST.get('alertEnabled') == 'on'

        category = Category.objects.get(id=category_id)

        Budget.objects.create(
            user=request.user,
            category=category,
            limit=limit,
            end_date=end_date + '-01',
            over_limit_alert=over_limit_alert
        )
        return redirect('/budget/')

    return render(request, 'budget.html', {'categories': categories})


@login_required
def budget_list(request):
    budgets = Budget.objects.filter(user=request.user)
    categories = Category.objects.all().filter(type='e')
    return render(request, 'budget.html', {'budgets': budgets , 'categories': categories})

@login_required
def budget_edit(request, pk):
    budget = Budget.objects.get(id=pk, user=request.user)
    categories = Category.objects.all()

    if request.method == 'POST':
        category_id = request.POST.get('category')
        limit = request.POST.get('amount')
        end_date = request.POST.get('period')
        over_limit_alert = request.POST.get('alertEnabled') == 'on'

        category = Category.objects.get(id=category_id)

        budget.category = category
        budget.limit = limit
        budget.end_date = end_date + '-01'
        budget.over_limit_alert = over_limit_alert
        budget.save()
        return redirect('/budget/')

    return redirect('/budget/')

@login_required
def budget_delete(request, pk):
    budget = Budget.objects.get(id=pk, user=request.user)
    if request.method == 'POST':
        budget.delete()
        return redirect('/budget/')
    return render(request, 'budget_confirm_delete.html', {'budget': budget})