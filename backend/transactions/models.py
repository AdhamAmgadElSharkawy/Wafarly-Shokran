from django.db import models 
from django.conf import settings
from decimal import Decimal
from django.utils import timezone

# Create your models here.
class Category(models.Model):
    name=models.CharField(max_length=50)
    type_choices = [('i', 'income'), ('e', 'expense')]
    type = models.CharField(max_length=1, choices=type_choices, default='e')
    def __str__(self):
        return self.name

class Transaction(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    category=models.ForeignKey(Category,on_delete=models.CASCADE)

    type_choices=[('i','income'),('e','expense')]
    type=models.CharField(max_length=15,choices=type_choices)
    description=models.TextField(null=True,blank=True)
    amount=models.DecimalField(max_digits=10,decimal_places=2)
    date_time=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.type}-{self.amount}'

    def save(self, *args, **kwargs):
        is_new = self.pk is None 

        super().save(*args, **kwargs)

        if is_new:
            from budget.models import Budget
            
            print(f"--- DEBUG: 1. Is New? {is_new} | Type: {self.type} ---")

            transaction_date = timezone.now().date()
            print(f"--- DEBUG: 3. Transaction Date is: {transaction_date} ---")

            budgets_to_update = Budget.objects.filter(
                user=self.user,
                category=self.category,
                start_date__lte=transaction_date,
                end_date__gte=transaction_date
            )
            
            for budget in budgets_to_update:
                budget.current += Decimal(self.amount)
                budget.save(update_fields=['current'])
