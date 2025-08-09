from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.utils import timezone

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    phone=models.CharField(max_length=15)
    address=models.TextField(blank=True)

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username


class MyCircle(models.Model):
    name=models.CharField(max_length=100)
    description=models.CharField(max_length=100)
    created_by=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    members=models.ManyToManyField(settings.AUTH_USER_MODEL,related_name='joined_circles',blank=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Expense(models.Model):
    description=models.CharField(max_length=100)
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    amount=models.DecimalField(max_digits=10,decimal_places=2)
    date=models.DateField()
    circle=models.ForeignKey(MyCircle,on_delete=models.CASCADE)
    category=models.ForeignKey(Category,on_delete=models.SET_NULL,null=True)

    def __str__(self):
        return f"{self.description} - ₹{self.amount} by {self.user.username}"

class Motivation(models.Model):
    quote=models.TextField()

    def __str__(self):
        return self.quote









