from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
import json

from .models import Transaction, Category

@login_required
def transaction_page(request):
    transactions = Transaction.objects.filter(user=request.user).order_by('-date_time')
    #return render(request, 'transaction.html', {"transactions": transactions})
    categories = Category.objects.all() 
    return render(request, 'transaction.html', {
        "transactions": transactions,
        "categories": categories
    })



def add_transaction(request):
    if request.method == "POST":
        data = json.loads(request.body)

        category = get_object_or_404(Category, id=data.get("category_id"))

        Transaction.objects.create(
            user=request.user,
            category=category,
            type=data.get("type"),
            description=data.get("description"),
            amount=data.get("amount")
        )

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
