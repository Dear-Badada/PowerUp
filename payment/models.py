from django.db import models

from powerbank.models import PowerBank
from users.models import User


class Order(models.Model):
    """ Order model """
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    power_bank = models.ForeignKey(PowerBank, on_delete=models.SET_NULL, null=True)
    deposit = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    hourly_rate = models.DecimalField(max_digits=10, decimal_places=2, null=False)  # 租借时的单价
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    order_status = models.CharField(max_length=10)
    payment_status = models.CharField(max_length=10)
    feedback = models.CharField(max_length=10)

    class Meta:
        db_table = "orders"

    def __str__(self):
        return f"Order {self.id} - {self.user.username}"


class Transaction(models.Model):
    """ Transaction model """
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)
    type = models.CharField(max_length=10)
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "transactions"

    def __str__(self):
        return f"Transaction {self.id} - {self.type} - {self.amount}"



class RefundRequest(models.Model):
    """ Refund request model """
    id = models.AutoField(primary_key=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reason = models.TextField(null=False)
    status = models.CharField(max_length=10)
    processed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "refund_requests"

    def __str__(self):
        return f"Refund Request {self.id} - Status: {self.status}"