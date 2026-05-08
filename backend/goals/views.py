from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Goal
from decimal import Decimal
from django.utils import timezone

@login_required
def goal_list(request):
    """
    Retrieves and displays a list of all saving goals for the authenticated user.
    
    Dynamically checks the deadline of each goal against the current time. 
    If the deadline has passed, it ensures the goal's status is updated.
    """
    goals = Goal.objects.filter(user=request.user)
    for goal in goals:
        if goal.deadline <= timezone.now():
            goal.iscompleted = False
            goal.save()
    return render(request, 'goals.html', {'goals': goals})

@login_required
def goal_create(request):
    """
    Handles the creation of a new financial goal.
    
    If the request is POST, extracts the goal details (title, target amount, dates)
    and creates a new Goal object linked to the current user, initialized as incomplete.
    """
    if request.method == 'POST':
        title = request.POST.get('title')
        target_amount = request.POST.get('target_amount')
        start_date = request.POST.get('start_date')
        deadline = request.POST.get('deadline')

        Goal.objects.create(
            user=request.user,
            title=title,
            target_amount=target_amount,
            start_date=start_date,
            deadline=deadline,
            iscompleted=False
        )
        return redirect('/goals/')

    return render(request, 'goals.html')

@login_required
def goal_edit(request, pk):
    """
    Handles updating the details of an existing goal.
    
    Fetches the goal by its primary key. On a POST request, updates its fields.
    Also checks if the updated target_amount has already been met by the current_amount,
    and updates the 'iscompleted' status accordingly.
    """
    goal = get_object_or_404(Goal, pk=pk, user=request.user)

    if request.method == 'POST':
        goal.title = request.POST.get('title')
        goal.target_amount = request.POST.get('target_amount')
        goal.start_date = request.POST.get('start_date')
        goal.deadline = request.POST.get('deadline')
        if goal.current_amount >= Decimal(request.POST.get('target_amount')):
            goal.iscompleted = True
        goal.save()
        return redirect('/goals/')
    

    return render(request, 'goals.html', {'goal': goal})

@login_required
def goal_delete(request, pk):
    """
    Handles the deletion of a specific goal.
    
    Requires a POST request to execute the deletion for security.
    Redirects back to the goals list upon successful deletion.
    """
    goal = get_object_or_404(Goal, pk=pk, user=request.user)
    if request.method == 'POST':
        goal.delete()
        return redirect('/goals/')
    return render(request, 'goals.html', {'goal': goal})
    
@login_required
def add_funds(request, pk):
    """
    Adds funds to the current progress of a specific goal.
    
    On a POST request, retrieves the added amount, increments the goal's current_amount,
    and checks if the goal's target_amount has been reached or exceeded. 
    If so, marks the goal as completed.
    """
    goal = get_object_or_404(Goal, pk=pk, user=request.user)
    if request.method == 'POST':
        amount = request.POST.get('amount')
        goal.current_amount += Decimal(amount)
        if goal.current_amount >= goal.target_amount:
            goal.iscompleted = True
        goal.save()
    return redirect('/goals/')

    