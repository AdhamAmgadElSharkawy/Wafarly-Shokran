from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Budget
from transactions.models import Category

@login_required
def budget_create(request):
    """
    Handles the creation of a new budget for the authenticated user.
    
    If the request method is POST, extracts form data to create a new Budget instance.
    Otherwise, renders the budget creation form with available categories.
    """
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
            end_date=end_date,
            over_limit_alert=over_limit_alert
        )
        return redirect('/budget/')

    return render(request, 'budget.html', {'categories': categories})


@login_required
def budget_list(request):
    """
    Retrieves and displays a list of all budgets for the authenticated user.
    Also fetches expense categories ('e') to populate the budget creation/edit forms.
    """
    budgets = Budget.objects.filter(user=request.user)
    categories = Category.objects.all().filter(type='e')
    return render(request, 'budget.html', {'budgets': budgets , 'categories': categories})

@login_required
def budget_edit(request, pk):
    """
    Handles updating an existing budget.
    
    Fetches the user's budget by its primary key (pk) and updates its fields
    if a POST request is received. Redirects back to the budget list afterwards.
    """
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
        budget.end_date = end_date
        budget.over_limit_alert = over_limit_alert
        budget.save()
        return redirect('/budget/')

    return redirect('/budget/')

@login_required
def budget_delete(request, pk):
    """
    Handles the deletion of a specific budget.
    
    If the request method is POST, deletes the budget identified by pk 
    for the current user and redirects to the budget list.
    Otherwise, renders a confirmation page for the deletion.
    """
    budget = Budget.objects.get(id=pk, user=request.user)
    if request.method == 'POST':
        budget.delete()
        return redirect('/budget/')
    return render(request, 'budget_confirm_delete.html', {'budget': budget})