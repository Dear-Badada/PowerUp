from django.db import models
import hashlib
import uuid

class User(models.Model):
    """ 用户模型 """
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=50, unique=True, null=False)
    email = models.EmailField(max_length=100, unique=True, null=False)
    phone = models.CharField(max_length=20, unique=True, null=False)
    password_hash = models.CharField(max_length=128, null=False)
    salt = models.CharField(max_length=64, null=False)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'phone']

    class Meta:
        db_table = "users"

    def __str__(self):
        return self.username

    def set_password(self, raw_password):
        """ Hash 用户密码 """
        self.salt = uuid.uuid4().hex  # 生成随机 salt
        hashed_password = hashlib.sha256((raw_password + self.salt).encode()).hexdigest()
        self.password_hash = hashed_password  # 存储 hash 后的密码

    def check_password(self, raw_password):
        """ 检查用户输入的密码是否正确 """
        hashed_password = hashlib.sha256((raw_password + self.salt).encode()).hexdigest()
        return self.password_hash == hashed_password
