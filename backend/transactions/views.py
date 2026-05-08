from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.core.mail import send_mail
from django.conf import settings
from decimal import Decimal
import json

from .models import Transaction, Category
from budget.models import Budget

@login_required
def transaction_page(request):
    """
    Renders the main transactions page for the application.
    
    Fetches all transactions associated with the logged-in user, ordered descending 
    by date and time (most recent first). It also provides all available categories 
    to populate the frontend forms.
    """
    transactions = Transaction.objects.filter(user=request.user).order_by('-date_time')
    #return render(request, 'transaction.html', {"transactions": transactions})
    categories = Category.objects.all() 
    return render(request, 'transaction.html', {
        "transactions": transactions,
        "categories": categories
    })

def check_budget_and_alert(user, category):
    """
    Evaluates current spending against the user's active budget for a specific category.
    
    Fetches the active budget where email alerts are explicitly enabled. If the 
    current spent amount (`budget.current`) equals or exceeds 80% of the defined 
    `budget.limit`, an automated email notification is dispatched to the user 
    using Django's SMTP backend to warn them about their spending rate.
    """
    budget = Budget.objects.filter(user=user,category=category,over_limit_alert=True).first()
    if not budget:
        return  
    Warning_limit = budget.limit*Decimal('0.80')
    if budget.current >= Warning_limit:
        subject = f"Wafarly Shokran Alert: ⚠️ Budget limit approaching for {category.name}"
        message = (
            f"Hello {user.first_name or user.username},\n\n"
            f"You have spent {budget.current} EGP on {category.name} this month.\n"
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
    """
    Creates a newly recorded financial transaction via an AJAX POST request.
    
    Parses the incoming JSON payload to instantiate and save a new Transaction. 
    If the specified transaction type evaluates to an expense ('e'), it automatically 
    triggers the `check_budget_and_alert` utility to verify if the user has 
    exceeded their 80% budget threshold and requires an email warning.
    """
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
    """
    Deletes a specific transaction securely via an AJAX POST request.
    
    Before the transaction is removed from the database, the function queries 
    for any active budgets matching the user, category, and date of the transaction. 
    If a corresponding budget is found, the transaction's amount is safely deducted 
    from the budget's `current` total to maintain absolute financial synchronization.
    """
    if request.method == "POST":
        transaction = get_object_or_404(Transaction, id=id, user=request.user)
        budget = Budget.objects.filter(user=transaction.user,category=transaction.category,start_date__lte=transaction.date_time.date(),end_date__gte=transaction.date_time.date())
        for B in budget:
            B.current -=Decimal( transaction.amount)
            B.save()
        transaction.delete()
        return JsonResponse({"status": "deleted"})


def edit_transaction(request, id):
    """
    Provides endpoints for retrieving and modifying existing transaction data via AJAX.
    
    On a GET request, it returns the current transaction attributes serialized as JSON 
    to seamlessly populate frontend modal forms. On a POST request, it extracts 
    updated details from the JSON payload, assigns them to the targeted Transaction 
    instance, and commits the changes to the database.
    """
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