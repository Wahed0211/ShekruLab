from django.db import models
from django.contrib.auth.models import User

class Payment(models.Model):
    razorpay_order_id = models.CharField(max_length=255, unique=True)
    razorpay_payment_id = models.CharField(max_length=255, blank=True, default="")
    amount = models.IntegerField()
    currency = models.CharField(max_length=3)
    status = models.CharField(max_length=50)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.TextField()
    company = models.CharField(max_length=255)
    phone = models.CharField(max_length=15)
    plan = models.CharField(max_length=50)

    def __str__(self):
        return self.user.username
