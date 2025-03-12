from django.db import models
from django.conf import settings

class Pricing(models.Model):
    hourly_rate = models.DecimalField(max_digits=10, decimal_places=2, default=1.00)
    deposit_amount = models.DecimalField(max_digits=10, decimal_places=2, default=15.00)

    def __str__(self):
        return f"Hourly Rate: £{self.hourly_rate}, Deposit: £{self.deposit_amount}"

class Order(models.Model):
    ORDER_STATUS_CHOICES = [
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
        ('canceled', 'Canceled'),
    ]

    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('refunded', 'Refunded'),
    ]

    FEEDBACK_CHOICES = [
        ('normal', 'Normal'),
        ('abnormal', 'Abnormal'),
    ]

    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    power_bank = models.ForeignKey('powerbank.PowerBank', on_delete=models.SET_NULL, null=True)
    deposit = models.DecimalField(max_digits=10, decimal_places=2)
    hourly_rate = models.DecimalField(max_digits=10, decimal_places=2)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    order_status = models.CharField(max_length=10, choices=ORDER_STATUS_CHOICES, default='ongoing')
    payment_status = models.CharField(max_length=10, choices=(
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('refunded', 'Refunded')),
        default='pending'
    )
    feedback = models.CharField(max_length=10, choices=(
        ('normal', 'Normal'),
        ('abnormal', 'Abnormal')),
        default='normal'
    )
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"Order #{self.id} - User: {self.user.username}"

class Transaction(models.Model):
    TRANSACTION_TYPE_CHOICES = [
        ('deposit', 'Deposit'),
        ('rental_fee', 'Rental Fee'),
        ('refund', 'Refund'),
        ('top-up', 'Top-up'),
    ]

    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)
    type = models.CharField(max_length=10, choices=TRANSACTION_TYPE_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.type.title()} £{self.amount:.2f} ({self.created_at.strftime('%Y-%m-%d %H:%M')})"

class RefundRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    reason = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    processed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Refund Request #{self.id} - Order #{self.order.id}"
