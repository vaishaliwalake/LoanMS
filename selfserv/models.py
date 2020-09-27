from django.db import models
from django.contrib.auth.models import AbstractUser

class Customers(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email=models.EmailField()
    CreditScore=models.IntegerField()
    RequestedLoanAmount=models.IntegerField()
    DurationInMonths=models.IntegerField()
    cust_id=models.IntegerField(default=None)

class Login(AbstractUser):
    id = models.AutoField(primary_key=True)
    password = models.CharField(max_length=12, default=None)
    username = models.CharField(max_length=12, unique=True, default=None)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email=models.EmailField()

