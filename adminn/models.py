from django.db import models
from django.contrib.auth.hashers import make_password, check_password
import datetime

class Admin(models.Model):
    """ Admin model """
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=50, unique=True, null=False)
    email = models.EmailField(max_length=100, unique=True, null=False)
    password_hash = models.CharField(max_length=128, null=False)
    created_at = models.DateTimeField(default=datetime.datetime.now)

    class Meta:
        db_table = "admins"

    def __str__(self):
        return self.username

    def set_password(self, raw_password):
        """ 使用 Django 内置方法存储加密密码 """
        self.password_hash = make_password(raw_password)

    def check_password(self, raw_password):
        """ 验证密码 """
        return check_password(raw_password, self.password_hash)
