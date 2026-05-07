from django.db import models
from django.conf import settings

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
    date_time=models.DateTimeField()

    def __str__(self):
        return f'{self.type}-{self.amount}'
