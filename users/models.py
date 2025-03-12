from django.db import models
import hashlib
import uuid

class User(models.Model):

    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=50, unique=True, null=False)
    email = models.EmailField(max_length=100, unique=True, null=False)
    phone = models.CharField(max_length=20, unique=True, null=False)
    password_hash = models.TextField(null=False)  # Explicitly store hashed password
    salt = models.TextField(null=False)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'phone']

    class Meta:
        db_table = "users"

    def __str__(self):
        return self.username

    def set_password(self, raw_password):
        # Hash the password and store it in password_hash field
        self.salt = uuid.uuid4().hex  # Generate a random salt
        hashed_password = hashlib.sha256((raw_password + self.salt).encode()).hexdigest()
        self.password_hash = hashed_password  # Store the hashed password in password_hash

    def check_password(self, raw_password):
        # Check the password by hashing it and comparing it with password_hash and salt
        hashed_password = hashlib.sha256((raw_password + self.salt).encode()).hexdigest()
        return self.password_hash == hashed_password