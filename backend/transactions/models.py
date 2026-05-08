from django.db import models 
from django.conf import settings
from decimal import Decimal
from django.utils import timezone

# Create your models here.
class Category(models.Model):
    """
    Represents a financial category for transactions and budgets.
    
    Attributes:
        name (CharField): The name of the category (e.g., 'Food', 'Salary').
        type (CharField): Categorizes as 'i' (income) or 'e' (expense).
    """
    name=models.CharField(max_length=50)
    type_choices = [('i', 'income'), ('e', 'expense')]
    type = models.CharField(max_length=1, choices=type_choices, default='e')
    def __str__(self):
        """Returns the string representation of the category."""
        return self.name

class Transaction(models.Model):
    """
    Represents a single financial transaction made by the user.
    
    Attributes:
        user (ForeignKey): The user who made the transaction.
        category (ForeignKey): The category the transaction belongs to.
        type (CharField): The type of transaction ('i' for income, 'e' for expense).
        description (TextField): Optional note or description.
        amount (DecimalField): The monetary value of the transaction.
        date_time (DateTimeField): Timestamp of when the transaction occurred.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    category=models.ForeignKey(Category,on_delete=models.CASCADE)

    type_choices=[('i','income'),('e','expense')]
    type=models.CharField(max_length=15,choices=type_choices)
    description=models.TextField(null=True,blank=True)
    amount=models.DecimalField(max_digits=10,decimal_places=2)
    date_time=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Returns a string showing the transaction type and amount."""
        return f'{self.type}-{self.amount}'

    def save(self, *args, **kwargs):
        """
        Overrides the default save method to automatically update active budgets.
        
        When a new transaction is created, it checks if there is an active budget 
        for the same user and category covering the current date. If found, 
        it increments the budget's current spent amount by the transaction amount.
        """
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
                start_date__lte=self.date_time.date(),
                end_date__gte=self.date_time.date()
            )
            
            for budget in budgets_to_update:
                budget.current += Decimal(self.amount)
                budget.save(update_fields=['current'])
