from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
import hashlib
import uuid

class User(AbstractBaseUser, PermissionsMixin):
    """ 用户模型 """
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=50, unique=True, null=False)
    email = models.EmailField(max_length=100, unique=True, null=False)
    phone = models.CharField(max_length=20, unique=True, null=False)
    password = models.CharField(max_length=128, null=False)
    salt = models.CharField(max_length=64, null=False)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)

    # Django 认证系统字段
    is_active = models.BooleanField(default=True)  # 用户是否激活
    is_staff = models.BooleanField(default=False)  # 是否有后台管理权限
    is_superuser = models.BooleanField(default=False)  # 是否是超级管理员

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'phone']

    class Meta:
        db_table = "users"

    def __str__(self):
        return self.username

    def set_password(self, raw_password):
        """ 生成随机 salt，并存储加密后的密码 """
        self.salt = uuid.uuid4().hex  # 生成随机 salt
        self.password = hashlib.sha256((raw_password + self.salt).encode()).hexdigest()  # 生成 hash

    def check_password(self, raw_password):
        """ 验证用户输入的密码是否正确 """
        hashed_password = hashlib.sha256((raw_password + self.salt).encode()).hexdigest()
        return hashed_password == self.password