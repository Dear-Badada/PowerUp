from django.db import models

class Station(models.Model):
    """ Station model """
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, null=False)
    location = models.TextField(null=False)

    class Meta:
        db_table = "stations"

    def __str__(self):
        return self.name


class PowerBank(models.Model):
    """ power bank model """
    id = models.AutoField(primary_key=True)
    station = models.ForeignKey(Station, on_delete=models.CASCADE)  # 关联站点
    battery_level = models.IntegerField(null=False, choices=[(i, i) for i in range(0, 101)])  # 电量在0到100之间
    status = models.CharField(
        max_length=10,
        default='available'
    )

    class Meta:
        db_table = "power_banks"

    def __str__(self):
        return f"PowerBank {self.id} - {self.status}"


class Pricing(models.Model):
    """ Pricing model """
    id = models.AutoField(primary_key=True)
    hourly_rate = models.DecimalField(max_digits=10, decimal_places=2, default=1.00)  # 每小时租赁费用
    deposit_amount = models.DecimalField(max_digits=10, decimal_places=2, default=15.00)  # 押金金额

    class Meta:
        db_table = "pricing"

    def __str__(self):
        return f"Hourly rate: {self.hourly_rate}, Deposit: {self.deposit_amount}"