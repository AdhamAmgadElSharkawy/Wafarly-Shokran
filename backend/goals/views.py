from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Goal
from decimal import Decimal

@login_required
def goal_list(request):
    goals = Goal.objects.filter(user=request.user)
    return render(request, 'goals.html', {'goals': goals})

@login_required
def goal_create(request):
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
    goal = get_object_or_404(Goal, pk=pk, user=request.user)

    if request.method == 'POST':
        goal.title = request.POST.get('title')
        goal.target_amount = request.POST.get('target_amount')
        goal.start_date = request.POST.get('start_date')
        goal.deadline = request.POST.get('deadline')
        goal.save()
        return redirect('/goals/')
    

    return render(request, 'goals.html', {'goal': goal})

@login_required
def goal_delete(request, pk):
    goal = get_object_or_404(Goal, pk=pk, user=request.user)
    if request.method == 'POST':
        goal.delete()
        return redirect('/goals/')
    return render(request, 'goals.html', {'goal': goal})

@login_required
def goal_mark_completed(request, pk):
    goal = get_object_or_404(Goal, pk=pk, user=request.user)
    goal.iscompleted = True
    goal.save()
    return redirect('/goals/')

@login_required
def add_funds(request, pk):
    goal = get_object_or_404(Goal, pk=pk, user=request.user)
    if request.method == 'POST':
        amount = request.POST.get('amount')
        goal.current_amount += Decimal(amount)
        if goal.current_amount >= goal.target_amount:
            goal.iscompleted = True
        goal.save()
    return redirect('/goals/')