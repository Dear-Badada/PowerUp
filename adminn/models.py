from django.db import models

class Admin(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    password_hash = models.TextField()
    salt = models.TextField()

    def __str__(self):
        return self.username