from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class PowerBank(models.Model):
    id = models.AutoField(primary_key=True)
    battery_level = models.IntegerField(default=100)
    status = models.CharField(max_length=20, choices=[('available', 'Available'), ('in_use', 'In Use')], default='available')

    def __str__(self):
        return f"PowerBank {self.id} - {self.status}"

class Rental(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    powerbank = models.ForeignKey(PowerBank, on_delete=models.CASCADE)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Rental {self.id} - {self.user.username}"
