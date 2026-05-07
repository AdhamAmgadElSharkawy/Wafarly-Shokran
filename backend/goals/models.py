from django.db import models
from django.conf import settings 
from transactions.models import Category
# Create your models here.

class Goal(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    title=models.CharField(max_length=50)
    target_amount=models.DecimalField(max_digits=10,decimal_places=2)
    current_amount=models.DecimalField(max_digits=10,decimal_places=2,default=0)
    iscompleted=models.BooleanField()
    start_date=models.DateField()
    deadline=models.DateTimeField()
    def __str__(self):
        return self.title


class Budget(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    limit=models.DecimalField(max_digits=10,decimal_places=2)
    end_date=models.DateField()
    over_limit_alert=models.BooleanField()

    def __str__(self):
        return f"{self.category.name} Budget - {self.limit_amount}"

