from django.db import models
from django.conf import settings 
from transactions.models import Category
# Create your models here.

class Goal(models.Model):
    """
    Represents a financial saving goal set by the user.
    
    Attributes:
        user (ForeignKey): The user who owns this goal.
        title (CharField): The name or description of the goal (e.g., 'New Car').
        target_amount (DecimalField): The total amount of money the user aims to save.
        current_amount (DecimalField): The amount saved so far (defaults to 0).
        iscompleted (BooleanField): Status flag indicating whether the goal has been achieved.
        start_date (DateField): The date the user started saving for this goal.
        deadline (DateTimeField): The target date and time to achieve the goal.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    title=models.CharField(max_length=50)
    target_amount=models.DecimalField(max_digits=10,decimal_places=2)
    current_amount=models.DecimalField(max_digits=10,decimal_places=2,default=0)
    iscompleted=models.BooleanField()
    start_date=models.DateField()
    deadline=models.DateTimeField()
    def __str__(self):
        """
        Returns the string representation of the goal (its title).
        """
        return self.title


