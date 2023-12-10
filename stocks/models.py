from django.db import models
from django.conf import settings


class Stock(models.Model):
    name = models.CharField(max_length=100, primary_key=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField(default=10000)


class Market(models.Model):
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    timestamp = models.DateTimeField()
    price = models.DecimalField(max_digits=10, decimal_places=2)


class Investor(models.Model):
    name = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    purchased_shares = models.IntegerField(default=0)


class Transaction(models.Model):
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    investor = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=10)  # Buy or Sell
    quantity = models.PositiveIntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)
