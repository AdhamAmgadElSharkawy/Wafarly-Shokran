from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    """
    Custom User model for the application.
    Extends Django's default AbstractUser to include additional fields.
    
    Attributes:
        birth_date (DateField): The user's date of birth (optional).
        phone_number (CharField): The user's contact number (optional).
    """
    birth_date=models.DateField(null=True,blank=True)
    phone_number=models.CharField(max_length=15,null=True,blank=True)
    def __str__(self):
        """
        Returns the string representation of the user (username).
        """
        return self.username