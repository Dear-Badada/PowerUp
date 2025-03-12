from django.db import models
from users.models import User

class Station(models.Model):
    name = models.CharField(max_length=100)
    location = models.TextField()

    def __str__(self):
        return self.name

class PowerBank(models.Model):
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('rented', 'Rented'),
        ('damaged', 'Damaged'),
    ]

    station = models.ForeignKey(Station, on_delete=models.CASCADE,null=True)
    battery_level = models.IntegerField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='available')

    def __str__(self):
        return f"PowerBank {self.id} - {self.status}"

class Rental(models.Model):
    ORDER_STATUS = [
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
        ('canceled', 'Canceled')
    ]
    PAYMENT_STATUS = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('refunded', 'Refunded')
    ]
    FEEDBACK = [
        ('normal', 'Normal'),
        ('abnormal', 'Abnormal')
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    power_bank = models.ForeignKey(PowerBank, on_delete=models.SET_NULL, null=True)
    deposit = models.DecimalField(max_digits=10, decimal_places=2, default=15.00)  # 已修正
    hourly_rate = models.DecimalField(max_digits=10, decimal_places=2, default=1.00)  # ← 增加了默认值
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    order_status = models.CharField(max_length=10, choices=ORDER_STATUS, default='ongoing')
    payment_status = models.CharField(max_length=10, choices=PAYMENT_STATUS, default='pending')
    feedback = models.CharField(max_length=10, choices=FEEDBACK, default='normal')

    def __str__(self):
        return f"Rental #{self.id} - {self.user.username}"