from django.db import models
from django.conf import settings 
from transactions.models import Category

# Create your models here.
class Budget(models.Model):
    """
    Represents a financial budget set by the user for a specific expense category.
    
    Attributes:
        user (ForeignKey): The user who owns this budget.
        category (ForeignKey): The expense category this budget applies to.
        current (DecimalField): The current amount spent (defaults to 0).
        limit (DecimalField): The maximum allowed spending limit.
        start_date (DateField): The date the budget was created.
        end_date (DateField): The deadline or reset date for the budget.
        over_limit_alert (BooleanField): Flag to enable/disable email notifications when approaching the limit.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    current=models.DecimalField(max_digits=10,decimal_places=2,default=0)
    limit=models.DecimalField(max_digits=10,decimal_places=2)
    start_date=models.DateField(auto_now_add=True)
    end_date=models.DateField()
    over_limit_alert=models.BooleanField()

    def __str__(self):
        """
        Returns a string representation of the budget, showing category and limit.
        """
        return f"{self.category.name} Budget - {self.limit}"