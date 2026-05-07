from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Sum
from decimal import Decimal
import datetime
import json

from .models import Transaction, Category
from budget.models import Budget

@login_required
def transaction_page(request):
    transactions = Transaction.objects.filter(user=request.user).order_by('-date_time')
    #return render(request, 'transaction.html', {"transactions": transactions})
    categories = Category.objects.all() 
    return render(request, 'transaction.html', {
        "transactions": transactions,
        "categories": categories
    })

def check_budget_and_alert(user, category):
    budget = Budget.objects.filter(user=user,category=category,over_limit_alert=True).first()
    if not budget:
        return
    current_month = datetime.datetime.now().month
    current_year = datetime.datetime.now().year
    total_spent = Transaction.objects.filter(
        user=user,
        category=category,
        type='e',
        date_time__month=current_month,
        date_time__year=current_year
    ).aggregate(total=Sum('amount'))['total'] or Decimal('0.00')
    Warning_limit = budget.limit*Decimal('0.80')
    if total_spent >= Warning_limit:
        subject = f"Wafarly Shokran Alert: ⚠️ Budget limit approaching for {category.name}"
        message = (
            f"Hello {user.first_name or user.username},\n\n"
            f"You have spent {total_spent} EGP on {category.name} this month.\n"
            f"This is over 80% of your set limit ({budget.limit} EGP).\n\n"
            f"Please review your dashboard to manage your upcoming expenses.\n\n"
            f"Best regards,\nWafarly Shokran Team"
        )
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email],
            fail_silently=False,
        )

def add_transaction(request):
    if request.method == "POST":
        data = json.loads(request.body)

        category = get_object_or_404(Category, id=data.get("category_id"))
        trans_type = data.get("type")
        Transaction.objects.create(
            user=request.user,
            category=category,
            type=data.get("type"),
            description=data.get("description"),
            amount=data.get("amount")
        )
        if trans_type == 'e':
            check_budget_and_alert(request.user, category)

        return JsonResponse({"status": "success"})


def delete_transaction(request, id):
    if request.method == "POST":
        transaction = get_object_or_404(Transaction, id=id, user=request.user)
        transaction.delete()
        return JsonResponse({"status": "deleted"})


def edit_transaction(request, id):
    transaction = get_object_or_404(Transaction, id=id, user=request.user)

    if request.method == "POST":
        data = json.loads(request.body)

        category = get_object_or_404(Category, id=data.get("category_id"))

        transaction.description = data.get("description")
        transaction.amount = data.get("amount")
        transaction.category = category
        transaction.type = data.get("type")
        transaction.save()

        return JsonResponse({"status": "updated"})

    return JsonResponse({
        "description": transaction.description,
        "amount": str(transaction.amount),
        #"category": transaction.category.name,
        "category_id": transaction.category.id,
        "type": transaction.type
    })
